from __future__ import annotations

from typing import List

from shared.domain.bus.event import DomainEventSubscriber, EventBus
from shared.domain.model.valueobject.url import Url
from shared.domain.service.scraping.pagerequester import PageRequester, Request
from duplicates.check.domain.event.duplicitycheckcompleted import (
    DuplicityCheckCompleted,
)
from duplicates.check.domain.event.duplicitycheckrequested import (
    DuplicityCheckRequested,
)
from duplicates.check.domain.model.duplicate import (
    Duplicate,
    DuplicateRepository,
)
from duplicates.report.domain.model.report import ReportRepository
from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datatransformer import DataTransformer
from duplicates.check.domain.model.corpus import CorpusRepository
from duplicates.similarity.domain.service.minhashgenerator import (
    MinHashGenerator,
)
from duplicates.similarity.domain.model.minhash import MinHashRepository
from duplicates.check.domain.model.duplicitycheck import (
    DuplicityCheckRepository,
    DuplicityCheckId,
)


class ScrapPagesOnDuplicityCheckRequested(DomainEventSubscriber):
    def __init__(self, pages_scraper: PagesScraper):
        super().__init__()

        self._pages_scraper = pages_scraper

    def handle(self, domain_event: DuplicityCheckRequested) -> None:
        self._pages_scraper.scrap(
            [Url(address) for address in domain_event.urls],
            domain_event.tenant_id,
            domain_event.check_id,
            domain_event.corpus,
            domain_event.similarity_threshold,
        )


class PagesScraper:
    def __init__(
        self,
        report_repository: ReportRepository,
        corpus_repository: CorpusRepository,
        pages_requester: PageRequester,
        data_transformer: DataTransformer,
        minhash_generator: MinHashGenerator,
        minhash_repository: MinHashRepository,
        duplicate_repository: DuplicateRepository,
        event_bus: EventBus,
    ):
        self._report_repository = report_repository
        self._corpus_repository = corpus_repository
        self._pages_requester = pages_requester
        self._data_transformer = data_transformer
        self._minhash_generator = minhash_generator
        self._minhash_repository = minhash_repository
        self._duplicate_repository = duplicate_repository
        self._event_bus = event_bus

    def scrap(
        self,
        urls: List[Url],
        tenant_id: str,
        duplicity_check_id: str,
        corpus_name: str,
        similarity_threshold: float,
    ):
        corpus = self._corpus_repository.corpus_of_name(tenant_id, corpus_name)
        report = self._report_repository.last_of_tenant(tenant_id)

        pages = []
        for url in urls:
            request = Request(url)
            request.headers = corpus.request_headers
            request.excluded_tags = corpus.excluded_tags
            request.excluded_selectors = corpus.excluded_selectors
            request.selector_mapping = corpus.selector_mapping

            response = self._pages_requester.request(request)

            content = [section for section in response.content.values()]
            actual_url = url
            if response.is_redirection():
                actual_url = response.final_url

            pages.append(
                Page(actual_url, " ".join(content), response.datalayer)
            )

        clean_pages = self._data_transformer.transform(pages)

        minhashes = self._minhash_generator.generate(
            report.k_shingle_size,
            clean_pages,
        )

        report_minhashes = self._minhash_repository.get_all_of_tenant(
            tenant_id
        )

        for address, minhash in minhashes.items():
            for report_address, report_minhash in report_minhashes.items():
                if address == report_address:
                    continue

                similarity = minhash.jaccard(report_minhash)
                if similarity < similarity_threshold:
                    continue

                duplicate = Duplicate(
                    DuplicityCheckId(duplicity_check_id),
                    Url(address),
                    Url(report_address),
                    similarity,
                )

                self._duplicate_repository.save(duplicate)

        self._event_bus.publish(DuplicityCheckCompleted(duplicity_check_id))


class UpdateCheckStatusOnDuplicityCheckRequested(DomainEventSubscriber):
    def __init__(self, check_status_updater: CheckStatusUpdater):
        super().__init__()

        self._check_status_updater = check_status_updater

    def handle(self, domain_event: DuplicityCheckCompleted) -> None:
        self._check_status_updater.update(
            DuplicityCheckId(domain_event.check_id)
        )


class CheckStatusUpdater:
    def __init__(self, duplicity_check_repository: DuplicityCheckRepository):
        self._duplicity_check_repository = duplicity_check_repository

    def update(self, duplicity_check_id: DuplicityCheckId):
        duplicity_check = (
            self._duplicity_check_repository.duplicity_check_of_id(
                duplicity_check_id
            )
        )

        duplicity_check.complete()
        self._duplicity_check_repository.save(duplicity_check)

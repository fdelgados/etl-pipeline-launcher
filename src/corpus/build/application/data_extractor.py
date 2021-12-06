import re

from typing import List
import multiprocessing
from joblib import Parallel, delayed, parallel_backend

import shared.infrastructure.environment.globalvars as glob
from shared.domain.service.logging.logger import Logger
from shared.domain.bus.event import DomainEventSubscriber, EventBus
from shared.domain.errors.errors import Errors, ApplicationError
from shared.domain.model.valueobject.url import Url

from corpus.build.domain.event.build_started import BuildStarted
from corpus.build.domain.event.extraction_failed import ExtractionFailed
from corpus.build.domain.event.urls_retrieved import UrlsRetrieved
from corpus.build.domain.model.build import BuildId, Build, BuildRepository
from corpus.build.domain.service.pagerequester import (
    PageRequester,
    Request,
    Response,
    PageRequesterFatalError,
    RetrievalError,
)
from corpus.build.domain.service.url_source import UrlSource, UrlSourceError
from corpus.build.domain.model.page import (
    Page,
    PageRepository,
    UnableToSavePageError,
)
from corpus.build.domain.model.corpus import Corpus, CorpusRepository


class ExtractDataOnBuildStarted(DomainEventSubscriber):
    def __init__(
        self,
        page_requester: PageRequester,
        url_source: UrlSource,
        build_repository: BuildRepository,
        page_repository: PageRepository,
        corpus_repository: CorpusRepository,
        logger: Logger,
        event_bus: EventBus,
    ):
        super().__init__()

        self._page_requester = page_requester
        self._url_source = url_source
        self._build_repository = build_repository
        self._page_repository = page_repository
        self._corpus_repository = corpus_repository
        self._logger = logger
        self._event_bus = event_bus

    def handle(self, domain_event: BuildStarted) -> None:
        self._log("info", "Start content extraction")

        build = self._find_build(
            domain_event.tenant_id, BuildId(domain_event.build_id)
        )

        try:
            corpus = self._find_corpus(build)

            urls = self._retrieve_urls(corpus)

            self._event_bus.publish(
                UrlsRetrieved(build.tenant_id, build.id.value, len(urls))
            )

            with parallel_backend(
                "threading", n_jobs=multiprocessing.cpu_count()
            ):
                Parallel()(
                    delayed(self._retrieve_page_content())(url, build, corpus)
                    for url in urls
                )

            build.complete()

        except (
            PageRequesterFatalError,
            UrlSourceError,
            UnableToSavePageError,
            ApplicationError,
        ) as error:
            build.abort()

            self._log("critical", str(error))
        finally:
            try:
                self._build_repository.save(build)
                self._event_bus.publish(*build.pull_events())

            except RuntimeError as err:
                self._log("critical", str(err))

    def _find_build(self, tenant_id: str, build_id: BuildId) -> Build:
        build = self._build_repository.build_of_tenant_and_id(
            tenant_id, build_id
        )

        if not build:
            error = Errors.entity_not_found()

            self._log("critical", str(error))

            raise ApplicationError(error)

        return build

    def _find_corpus(self, build: Build) -> Corpus:
        corpus: Corpus = self._corpus_repository.corpus_of_tenant_and_name(
            build.tenant_id, build.corpus_name
        )

        if not corpus:
            raise ApplicationError(Errors.entity_not_found())

        return corpus

    def _retrieve_urls(self, corpus: Corpus) -> List[Url]:
        valid_urls = []
        limit = 100 if glob.settings.is_development() else 0

        urls = self._url_source.retrieve(
            max_urls=limit, sitemaps=corpus.sitemaps
        )

        for url in urls:
            if corpus.url_address_pattern and not re.fullmatch(
                corpus.url_address_pattern, url.address
            ):
                self._logger.warning("Invalid URL: {}".format(url))

                continue

            valid_urls.append(url)

        return valid_urls

    def _retrieve_page_content(self):
        def build_page(
            response: Response,
            corpus: Corpus,
            build: Build,
        ) -> Page:
            page = Page(
                response.url,
                build.id,
                build.tenant_id,
                response.status_code,
                response.status,
                response.modified_on,
                corpus.name,
            )

            if not response.is_successful:
                return page

            page.h1 = response.h1
            page.title = response.title
            if response.is_indexable:
                page.mark_as_indexable()

            page.canonical_url = response.canonical_url
            page.datalayer = response.datalayer
            page.content = response.content

            return page

        def retrieve_page_content(url: Url, build: Build, corpus: Corpus):
            try:
                request = Request(url)
                request.headers = corpus.request_headers
                request.excluded_tags = corpus.excluded_tags
                request.excluded_selectors = corpus.excluded_selectors
                request.selector_mapping = corpus.selector_mapping

                response = self._page_requester.request(request)

                page = build_page(response, corpus, build)

                self._page_repository.save(page)

                self._event_bus.publish(*page.pull_events())
            except RetrievalError as error:
                self._log("error", f"{url}: {str(error)}")

                self._publish_extraction_failed(build, url)

            except PageRequesterFatalError as error:
                self._log("critical", f"{url}: {str(error)}")

                self._publish_extraction_failed(build, url)

                raise
            except Exception as error:
                self._log("critical", f"{url}: {str(error)}")

                self._publish_extraction_failed(build, url)

        return retrieve_page_content

    def _publish_extraction_failed(self, build: Build, url: Url) -> None:
        self._event_bus.publish(
            ExtractionFailed(build.tenant_id, build.id.value, url.address)
        )

    def _log(self, level: str, message: str):
        module = self.__class__.__module__
        class_name = self.__class__.__qualname__

        message = f"{module}.{class_name}: {message}"

        if level == "warning":
            self._logger.warning(message)
        elif level == "error":
            self._logger.error(message)
        elif level == "critical":
            self._logger.critical(message)

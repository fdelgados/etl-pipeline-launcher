import re

from typing import List
import multiprocessing
from joblib import Parallel, delayed, parallel_backend

from shared import settings
from shared.domain.service.logging.logger import Logger
from shared.domain.bus.event import DomainEventSubscriber, EventBus

from corpus_builder.build.domain.event.build_started import BuildStarted
from corpus_builder.build.domain.event.extraction_failed import ExtractionFailed
from corpus_builder.build.domain.event.urls_retrieved import UrlsRetrieved
from corpus_builder.build.domain.model.build import BuildId, Build, BuildRepository
from corpus_builder.build.domain.model.url import Url
from corpus_builder.build.domain.service.content.page_retriever import (
    PageRetriever,
    PageRetrieverFatalError,
    RetrievalError,
)
from corpus_builder.build.domain.service.content.url_source import UrlSource
from corpus_builder.build.domain.model.page import PageRepository
from corpus_builder.corpus.domain.model.corpus import Corpus, CorpusRepository


class ExtractDataOnBuildStarted(DomainEventSubscriber):
    def __init__(
        self,
        page_retriever: PageRetriever,
        url_source: UrlSource,
        build_repository: BuildRepository,
        page_repository: PageRepository,
        corpus_repository: CorpusRepository,
        logger: Logger,
        event_bus: EventBus,
    ):
        self._page_retriever = page_retriever
        self._url_source = url_source
        self._build_repository = build_repository
        self._page_repository = page_repository
        self._corpus_repository = corpus_repository
        self._logger = logger
        self._event_bus = event_bus

    def subscribed_to(self) -> List:
        return [BuildStarted.type_name()]

    def handle(self, domain_event: BuildStarted) -> None:
        self._log("info", "Start content extraction")

        build: Build = self._build_repository.build_of_tenant_and_id(
            domain_event.tenant_id, BuildId(domain_event.build_id)
        )

        corpus: Corpus = self._corpus_repository.corpus_of_tenant_and_name(
            build.tenant_id, build.corpus_name
        )

        urls = self._retrieve_urls(corpus)

        self._event_bus.publish(
            UrlsRetrieved(build.tenant_id, build.id.value, len(urls))
        )

        with parallel_backend("threading", n_jobs=multiprocessing.cpu_count()):
            Parallel()(
                delayed(self._retrieve_page_content())(url, build, corpus)
                for url in urls
            )

        build.complete()
        self._build_repository.save(build)

        self._event_bus.publish(*build.pull_events())

    def _retrieve_urls(self, corpus: Corpus) -> List[Url]:
        valid_urls = []
        limit = 100 if settings.is_development() else 0

        urls = self._url_source.retrieve(max_urls=limit, sitemaps=corpus.sitemaps)

        for url in urls:
            if corpus.url_address_pattern and not re.fullmatch(
                corpus.url_address_pattern, url.address
            ):
                self._logger.warning("Invalid URL: {}".format(url))

                continue

            valid_urls.append(url)

        return valid_urls

    def _retrieve_page_content(self):
        def retrieve_page_content(url: Url, build: Build, corpus: Corpus):
            try:
                page = self._page_retriever.retrieve(url, build, corpus)

                self._page_repository.save(page)

                self._event_bus.publish(*page.pull_events())
            except RetrievalError as error:
                self._log("error", f"{url}: {str(error)}")

                self._publish_extraction_failed(build, url)

            except PageRetrieverFatalError as error:
                self._log("critical", f"{url}: {str(error)}")

                self._publish_extraction_failed(build, url)

                raise

        return retrieve_page_content

    def _publish_extraction_failed(self, build: Build, url: Url) -> None:
        self._event_bus.publish(
            ExtractionFailed(build.tenant_id, build.id.value, url.address)
        )

    def _log(self, level: str, message: str):
        message = (
            f"{self.__class__.__module__}.{self.__class__.__qualname__}: {message}"
        )

        if level == "warning":
            self._logger.warning(message)
        elif level == "error":
            self._logger.error(message)
        elif level == "critical":
            self._logger.critical(message)

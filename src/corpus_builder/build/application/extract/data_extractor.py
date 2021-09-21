import re

from typing import List
import multiprocessing
from joblib import Parallel, delayed, parallel_backend

from shared import settings
from shared.domain.service.logging.logger import Logger
from shared.infrastructure.event import DomainEventDispatcher

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


class ExtractDataOnBuildStarted:
    def __init__(
        self,
        page_retriever: PageRetriever,
        url_source: UrlSource,
        build_repository: BuildRepository,
        page_repository: PageRepository,
        corpus_repository: CorpusRepository,
        logger: Logger
    ):
        self._page_retriever = page_retriever
        self._url_source = url_source
        self._build_repository = build_repository
        self._page_repository = page_repository
        self._corpus_repository = corpus_repository
        self._logger = logger

    def __call__(self, event: BuildStarted) -> None:
        self._log("info", "Start content extraction")

        build: Build = self._build_repository.build_of_tenant_and_id(
            event.tenant_id, BuildId(event.build_id)
        )

        corpus_config: Corpus = self._corpus_repository.config_of_tenant_and_name(
            build.tenant_id,
            build.corpus_name
        )

        urls = self._retrieve_urls(corpus_config)

        DomainEventDispatcher.dispatch([
            UrlsRetrieved(build.tenant_id, build.id.value, len(urls))
        ])

        def scrape(url: Url):
            try:
                page = self._page_retriever.retrieve(url, build, corpus_config)

                self._page_repository.save(page)

                DomainEventDispatcher.dispatch(page.events())
            except RetrievalError as error:
                self._log("error", f"{url}: {str(error)}")

                _dispatch_extraction_failed(build, url)

            except PageRetrieverFatalError as error:
                self._log("critical", f"{url}: {str(error)}")

                _dispatch_extraction_failed(build, url)

                raise

        with parallel_backend("threading", n_jobs=multiprocessing.cpu_count()):
            Parallel()(delayed(scrape)(url) for url in urls)

        build.complete()
        self._build_repository.save(build)

        DomainEventDispatcher.dispatch(build.events())

    def _retrieve_urls(self, corpus_config: Corpus) -> List[Url]:
        valid_urls = []
        limit = 100 if settings.is_development() else 0

        urls = self._url_source.retrieve(max_urls=limit, sitemaps=corpus_config.sitemaps)

        for url in urls:
            if corpus_config.url_address_pattern and not re.fullmatch(corpus_config.url_address_pattern, url.address):
                self._logger.warning("Invalid URL: {}".format(url))

                continue

            valid_urls.append(url)

        return valid_urls

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


def _dispatch_extraction_failed(build: Build, url: Url):
    DomainEventDispatcher.dispatch([
        ExtractionFailed(build.tenant_id, build.id.value, url.address)
    ])

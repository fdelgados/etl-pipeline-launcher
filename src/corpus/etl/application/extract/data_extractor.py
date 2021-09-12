import re
from dataclasses import dataclass, field

from typing import List
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
from tqdm import tqdm

from shared import settings
from shared.domain.service.logging.logger import Logger

from corpus.etl.domain.model.etl import *
from corpus.etl.domain.model.url import Url
from corpus.etl.domain.service.content.page_retriever import *
from corpus.etl.domain.service.content.url_source import *
from shared.infrastructure.event import DomainEventPublisher
from corpus.etl.domain.event.extraction_started import ExtractionStarted
from corpus.etl.domain.event.extraction_completed import ExtractionCompleted
from corpus.etl.domain.model.page import Page, PageRepository


@dataclass(frozen=True)
class ExtractDataCommand:
    tenant_id: str
    etl_id: str
    sitemaps: List
    url_pattern: str = field(default=None)
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_tags: List[str] = field(default_factory=[])
    excluded_selectors: List[str] = field(default_factory=[])
    custom_fields: dict = field(default_factory={})


class DataExtractor:
    def __init__(
        self,
        page_retriever: PageRetriever,
        url_source: UrlSource,
        etl_repository: EtlRepository,
        page_repository: PageRepository,
        logger: Logger,
        progress_bar: Logger,
    ):
        self._page_retriever = page_retriever
        self._url_source = url_source
        self._etl_repository = etl_repository
        self._page_repository = page_repository
        self._logger = logger
        self._progress_bar = progress_bar

    def extract(self, command: ExtractDataCommand) -> None:
        self._log("info", "Start content extraction")

        etl: Etl = self._etl_repository.etl_of_tenant_and_id(
            command.tenant_id, EtlId(command.etl_id)
        )

        urls = self._retrieve_urls(
            etl.sitemaps,
            etl.url_address_pattern,
            limit=100 if settings.is_development() else 0,
        )
        number_of_urls = len(urls)

        DomainEventPublisher.publish([ExtractionStarted(etl.id.value)])

        def scrape(url: Url):
            try:
                page = self._page_retriever.retrieve(url, etl)

                self._page_repository.save(page)

                DomainEventPublisher.publish(page.events())
            except RetrievalError as error:
                self._log("error", f"{url}: {str(error)}")
            except PageRetrieverFatalError as error:
                self._log("critical", f"{url}: {str(error)}")

                raise

        with parallel_backend("threading", n_jobs=multiprocessing.cpu_count()):
            Parallel()(
                delayed(scrape)(url)
                for url in tqdm(urls, ascii=" #", desc="Extracting content from URLs")
            )

        DomainEventPublisher.publish(
            [ExtractionCompleted(command.etl_id, number_of_urls)]
        )

    def _retrieve_urls(
        self, sitemaps: List, url_pattern: str = None, limit: int = 0
    ) -> List[Url]:
        valid_urls = []

        urls = self._url_source.retrieve(max_urls=limit, sitemaps=sitemaps)

        for url in urls:
            if url_pattern and not re.fullmatch(url_pattern, url.address):
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

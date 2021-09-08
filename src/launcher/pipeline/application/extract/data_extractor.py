import re
from dataclasses import dataclass, field

from typing import List, Tuple, Dict
import multiprocessing
from joblib import Parallel, delayed, parallel_backend
from tqdm import tqdm

from shared import settings
from shared.domain.service.logging.logger import Logger
from launcher.pipeline.domain.model.pipeline import (
    Pipeline,
    PipelineId,
    PipelineRepository
)
from launcher.pipeline.domain.service.scraping import (
    Scraper,
    SitemapScraper,
    ScraperException,
    FatalScraperException
)
from shared.infrastructure.event import DomainEventPublisher
from launcher.pipeline.domain.event.extraction_started import ExtractionStarted
from launcher.pipeline.domain.event.extraction_completed import ExtractionCompleted
from launcher.pipeline.domain.model.page import Page, PageRepository


@dataclass(frozen=True)
class ExtractDataCommand:
    tenant_id: str
    pipeline_id: str
    sitemap_urls: Dict
    url_pattern: str = field(default=None)
    custom_request_headers: dict = field(default_factory={})
    selector_mapping: dict = field(default_factory={})
    excluded_tags: List[str] = field(default_factory=[])
    excluded_selectors: List[str] = field(default_factory=[])
    custom_fields: dict = field(default_factory={})


class DataExtractor:
    def __init__(
        self,
        scraper: Scraper,
        sitemap_scraper: SitemapScraper,
        pipeline_repository: PipelineRepository,
        page_repository: PageRepository,
        logger: Logger,
        progress_bar: Logger,
    ):
        self._scraper = scraper
        self._sitemap_scraper = sitemap_scraper
        self._pipeline_repository = pipeline_repository
        self._page_repository = page_repository
        self._logger = logger
        self._progress_bar = progress_bar

    def extract(self, command: ExtractDataCommand) -> None:
        self._log('info', 'Start content extraction')

        pipeline: Pipeline = self._pipeline_repository.pipeline_of_tenant_and_id(
            command.tenant_id,
            PipelineId(command.pipeline_id)
        )

        urls = self._retrieve_urls(
            pipeline.sitemaps_urls,
            pipeline.url_address_pattern,
            limit=100 if settings.is_development() else 0
        )
        number_of_urls = len(urls)

        DomainEventPublisher.publish(
            [ExtractionStarted(pipeline.id.value)]
        )

        def scrape(url):
            try:
                page = self._scraper.scrape(
                    url,
                    pipeline,
                    delay=0,
                    is_secure_connection=settings.is_production()
                )

                self._page_repository.save(page)

                DomainEventPublisher.publish(page.events())
            except ScraperException as error:
                self._log('error', f'{url}: {str(error)}')
            except FatalScraperException as error:
                self._log('critical', f'{url}: {str(error)}')

                raise

        with parallel_backend('threading', n_jobs=multiprocessing.cpu_count()):
            Parallel()(
                delayed(scrape)(url)
                for (url, _) in tqdm(urls, ascii=' #', desc='Extracting content from URLs')
            )

        DomainEventPublisher.publish([
            ExtractionCompleted(command.pipeline_id, number_of_urls)
        ])

    def _retrieve_urls(
        self,
        sitemaps_url: Dict,
        url_pattern: str = None,
        limit: int = 0
    ) -> List[Tuple[str, str]]:

        formatted_urls = []

        urls = self._sitemap_scraper.retrieve_urls(
            sitemaps_url,
            max_urls=limit
        )

        for url, data in urls:
            if url_pattern and not re.fullmatch(url_pattern, url):
                self._logger.warning('Invalid URL: {}'.format(url))

                continue

            formatted_urls.append((data['url'], data['lastmod'] if data['lastmod'] else None))

        return formatted_urls

    # def _save_page_content(self, page: Page):
    #     try:
    #         if page.is_unmodified():
    #             self._page_repository.update_status(page.address, page.status_code, page.status)
    #
    #             return
    #
    #         self._page_repository.save(page)
    #
    #         extra_info = self._extra_info(page)
    #         page_extracted = PageExtracted(
    #             self._report_id,
    #             page.address,
    #             page.status_code,
    #             page.status,
    #             page.h1,
    #             page.title,
    #             page.is_canonical,
    #             page.is_indexable,
    #             page.final_address,
    #             page.last_extracted_on,
    #             str(extra_info['id']) if extra_info['id'] is not None else None,
    #             str(extra_info['center_id']) if extra_info['center_id'] is not None else None,
    #             extra_info['center_name'],
    #             extra_info['methodology_id'],
    #             extra_info['country']
    #         )
    #
    #         self._event_publisher.dispatch(page_extracted)
    #
    #     except UnableToSavePageException as error:
    #         self._log_error(page.address, str(error))

    def _extra_info(self, page: Page):
        default_info = {
            'id': None,
            'center_id': None,
            'center_name': None,
            'methodology_id': None,
            'country': None
        }

        if not bool(page.datalayer):
            self._logger.warning('Unable to access to {} datalayer'.format(page.address))

            return default_info

        try:
            course = page.datalayer.get('course')
            course_id = course.get('id')
            country = re.sub(r'^([a-zA-Z]{2})[0-9]+$', r'\1', course.get('globalSearchId')).upper()
            center = course.get('center')
            center_id = center.get('id')
            center_name = center.get('name')
            methodology_id = int(course.get('methodology').get('id'))
        except Exception as e:
            self._logger.error(str(e))

            return default_info

        return {
            'id': course_id,
            'center_id': center_id,
            'center_name': center_name,
            'methodology_id': methodology_id,
            'country': country
        }

    def _log(self, level: str, message: str):
        message = f'{self.__class__.__module__}.{self.__class__.__qualname__}: {message}'

        if level == 'warning':
            self._logger.warning(message)
        elif level == 'error':
            self._logger.error(message)
        elif level == 'critical':
            self._logger.critical(message)

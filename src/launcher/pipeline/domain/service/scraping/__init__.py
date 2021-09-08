import abc

from typing import List, Dict

from launcher.pipeline.domain.model.page import Page
from launcher.pipeline.domain.model.url import Url
from launcher.pipeline.domain.model.pipeline import Pipeline


class ScraperException(RuntimeError):
    pass


class FatalScraperException(RuntimeError):
    pass


class Scraper(metaclass=abc.ABCMeta):
    def scrape(
        self,
        url: Url,
        pipeline: Pipeline,
        delay: int = 0,
        is_secure_connection: bool = False
    ) -> Page:
        raise NotImplementedError


class SitemapScraper(metaclass=abc.ABCMeta):
    def retrieve_urls(
        self,
        sitemap_urls: Dict,
        max_urls: int = 0
    ) -> List[Dict]:
        raise NotImplementedError

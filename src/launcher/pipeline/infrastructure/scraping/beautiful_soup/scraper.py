from __future__ import annotations

import os
import re
from typing import Optional, List, Dict
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError
import requests
from http import HTTPStatus
import pytz
from time import sleep

import urllib3
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from json import loads, decoder

from launcher.pipeline.domain.model.page import Page
from launcher.pipeline.domain.model.url import Url, InvalidUrlException
from launcher.pipeline.domain.model.pipeline import Pipeline
from launcher.pipeline.domain.service.scraping import (
    Scraper,
    SitemapScraper,
    ScraperException,
    FatalScraperException
)
from shared.domain.service.caching.cache import Cache

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BeautifulSoupWebScraper(Scraper):
    _PARSER = 'lxml'
    _STRING_SEPARATOR = ' '
    _ACTION_ON_429_STATUS = 'retry'  # or 'exit'
    _REQUEST_HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,ca;q=0.6,it;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.107 Safari/537.36'
    }
    _EXCLUDE_REQUEST_HEADERS = [
        'If-Modified-Since'
    ]
    _DEFAULT_BLACKLISTED_TAGS = [
        '[document]',
        'noscript',
        'header',
        'footer',
        'iframe',
        'html',
        'meta',
        'script',
        'br',
    ]

    def __init__(self, cache: Cache):
        self._cache = cache

    def scrape(
        self,
        url: Url,
        pipeline: Pipeline,
        delay: int = 0,
        is_secure_connection: bool = False
    ) -> Page:

        if delay > 0:
            sleep(delay)

        self._ensure_scraping_is_allowed(url)

        headers = self._request_headers(pipeline.request_headers)
        try:
            last_modified_on = self._last_extracted_date_cached(url)

            if last_modified_on:
                headers['If-Modified-Since'] = last_modified_on

            response = requests.get(
                url.address,
                allow_redirects=True,
                verify=is_secure_connection,
                headers=headers
            )

            self._ensure_is_a_valid_response(response)

            page = Page(
                url,
                pipeline.id,
                response.status_code,
                response.reason,
                _date_to_local(response.headers.get('Date'))
            )

            if response.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_MODIFIED]:
                return page

            if response.history:
                last_response = response.history[-1]

                page = Page(
                    url,
                    pipeline.id,
                    last_response.status_code,
                    last_response.reason,
                    _date_to_local(response.headers.get('Date'))
                )

                page.final_url = Url(response.url)

            if response.status_code == HTTPStatus.NOT_MODIFIED:
                return page

            self._cache_last_extracted_date(url.address, response.headers.get('Date'))

            markup_parser = MarkupParser(
                self._retrieve_content(response.content)
            )

            page.h1 = markup_parser.h1()
            page.title = markup_parser.title()
            if markup_parser.is_indexable(response):
                page.mark_as_indexable()

            page.canonical_url = markup_parser.canonical_version()
            page.datalayer = markup_parser.datalayer()

            blacklisted_tags = pipeline.excluded_tags
            blacklisted_tags.extend(self._DEFAULT_BLACKLISTED_TAGS)
            body = markup_parser.body(
                blacklisted_tags,
                pipeline.excluded_selectors
            )

            selector_mapping = pipeline.selector_mapping or {}
            page.content = self._build_content(body, **selector_mapping)

            return page
        except requests.exceptions.RequestException as error:
            raise ScraperException(str(error))

    def _build_content(self, body, **selectors):
        page_content = {}

        if selectors:
            for (name, selector) in selectors.items():
                selector_tags = body.select(selector)
                page_content[name] = self._STRING_SEPARATOR.join([
                    self._STRING_SEPARATOR.join(tag.get_text(self._STRING_SEPARATOR, strip=True).split())
                    for tag in selector_tags
                ])
        else:
            tags = body.find_all()

            page_content['body'] = self._STRING_SEPARATOR.join([
                self._STRING_SEPARATOR.join(tag.get_text(self._STRING_SEPARATOR, strip=True).split())
                for tag in tags
            ])

        return page_content

    def _ensure_scraping_is_allowed(self, url: Url) -> None:
        url_struct = urlparse(url.address)
        robots_url = '{}://{}/robots.txt'.format(
            url_struct.scheme,
            url_struct.netloc
        )

        robot_parser = RobotFileParser(robots_url)
        robot_parser.read()

        if not robot_parser.can_fetch(self._REQUEST_HEADERS.get('User-Agent'), url.address):
            raise ScraperException('robots.txt forbidden the scraping')

    def _request_headers(self, request_headers: Dict) -> Dict:
        clean_request_headers = {name: value for name, value in request_headers.items()
                                 if name not in self._EXCLUDE_REQUEST_HEADERS}

        return {**self._REQUEST_HEADERS, **clean_request_headers}

    def _ensure_is_a_valid_response(self, response):
        if response.status_code != HTTPStatus.TOO_MANY_REQUESTS:
            return

        if self._ACTION_ON_429_STATUS == 'exit':
            raise FatalScraperException(
                'The server responded with a status of {} {}'.format(response.status_code, response.reason)
            )

    def _retrieve_content(self, content: bytes):
        return BeautifulSoup(content, self._PARSER)

    def _last_extracted_date_cached(self, url: Url) -> Optional[str]:
        date = self._cache.read(url.address)
        if not date:
            return None

        return date.decode('utf-8')

    def _cache_last_extracted_date(self, url: str, date: str) -> None:
        self._cache.write(url, date)


def _date_to_local(gmt_date: str):
    date = datetime.strptime(gmt_date, '%a, %d %b %Y %H:%M:%S %Z')
    gmt_timezone = pytz.timezone('GMT')
    date = gmt_timezone.localize(date)

    return date.astimezone(pytz.timezone(os.environ['TZ']))


class MarkupParser:
    def __init__(self, markup):
        self.markup = markup

    def body(self, blacklisted_tags: List[str] = None, blacklisted_selectors: List[str] = None):
        try:
            body = self.markup.body

            if blacklisted_tags:
                for tag in body.find_all(name=set(blacklisted_tags)):
                    tag.decompose()

            if not blacklisted_selectors:
                return body

            for selector in body.select(','.join(set(blacklisted_selectors))):
                selector.decompose()

            return body
        except AttributeError:
            return None

    def title(self):
        try:
            return self.markup.title.get_text().strip()
        except AttributeError:
            return None

    def h1(self):
        try:
            return self.markup.body.h1.get_text().strip()
        except AttributeError:
            return None

    def canonical_version(self) -> Optional[Url]:
        canonical = self.markup.find('link', attrs={'rel': 'canonical'})

        if not canonical:
            return None

        return Url(canonical.attrs['href'])

    def is_indexable(self, response) -> bool:
        if 'X-Robots-Tag' not in response.headers:
            meta_robots = self.markup.find('meta', attrs={'name': 'robots'})

            if not meta_robots:
                return True

            return 'noindex' not in meta_robots.get('content')

        return 'noindex' not in response.headers.get('X-Robots-Tag')

    def datalayer(self) -> Dict:
        try:
            script_text = self.markup.find(string=re.compile(r'var\s+dataLayer')).split('= ', 1)[1]

            return loads(script_text[:script_text.find('];')] + ']')[0]
        except decoder.JSONDecodeError:
            return {}


class BeautifulSoupSitemapScraper(SitemapScraper):
    PARSER = 'xml'

    def __init__(self):
        self.__urls: Dict = {}

    def retrieve_urls(
        self,
        sitemap_urls: Dict,
        max_urls: int = 100
    ) -> List[Dict]:

        for sitemap_url, properties in sitemap_urls.items():
            child_sitemap_urls = self._sitemaps_urls(sitemap_url, properties)
            for child_sitemap_url in child_sitemap_urls:
                self._retrieve_from_sitemap(child_sitemap_url, max_urls)

        if max_urls > 0:
            return list(self.__urls.items())[:max_urls]

        return list(self.__urls.items())

    def _sitemaps_urls(self, sitemap_url: str, properties: Dict):
        if properties.get('root', False):
            return self._retrieve_sitemaps_from_root(sitemap_url, properties.get('sitemaps_url_pattern'))

        return [sitemap_url]

    def _retrieve_sitemaps_from_root(self, sitemap_url: str, sitemaps_url_pattern: Optional[str] = None):
        sitemap_urls = []
        try:
            root_sitemap_response = urlopen(sitemap_url)
            soup = BeautifulSoup(root_sitemap_response, self.PARSER)

            sitemap_nodes = soup.find_all('sitemap')

            for node in sitemap_nodes:
                url = node.find('loc').string

                if not sitemaps_url_pattern:
                    sitemap_urls.append(url)
                else:
                    if re.match(sitemaps_url_pattern, url):
                        sitemap_urls.append(url)
        except URLError as error:
            raise FatalScraperException(str(error))

        return sitemap_urls

    def _retrieve_from_sitemap(self, sitemap_url: str, max_urls: int):
        if 0 < max_urls <= len(self.__urls):
            return

        try:
            sitemap_response = urlopen(sitemap_url)
            soup = BeautifulSoup(sitemap_response, self.PARSER)

            nodes = soup.find_all('url')

            for node in nodes:
                address = str(node.find('loc').string)

                self.__urls[address] = {
                    'url': Url(address),
                    'lastmod': datetime.strptime(str(node.find('lastmod').string), '%Y-%m-%d'),
                    'priority': str(node.find('priority').string)
                }

                if 0 < max_urls <= len(self.__urls):
                    break
        except (URLError, InvalidUrlException) as error:
            raise FatalScraperException(str(error))

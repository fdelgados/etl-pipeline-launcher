from __future__ import annotations

import re
from typing import Optional, List, Dict
from urllib.request import urlopen
from urllib.error import URLError

import urllib3

from bs4 import BeautifulSoup

from corpus.etl.domain.model.url import Url, InvalidUrlException
from corpus.etl.domain.service.content.page_retriever import *
from corpus.etl.domain.service.content.url_source import *


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UrlSourceImpl(UrlSource):
    PARSER = "xml"

    def __init__(self):
        self.__urls: Dict = {}

    def retrieve(self, max_urls: int = 0, **kwargs) -> List[Url]:
        sitemaps = kwargs.get("sitemaps")

        if not sitemaps:
            raise UrlSourceError("You must provide a sitemap list")

        for sitemap in sitemaps:
            url = sitemap.get("url")
            sitemaps_url_pattern = sitemap.get("sitemaps_url_pattern", None)

            child_sitemap_urls = self._sitemaps_urls(url, sitemaps_url_pattern)
            for child_sitemap_url in child_sitemap_urls:
                self._retrieve_from_sitemap(child_sitemap_url, max_urls)

        if max_urls > 0:
            return list(self.__urls.values())[:max_urls]

        return list(self.__urls.values())

    def _sitemaps_urls(self, sitemap_url: str, sitemaps_url_pattern: Optional[str]):
        if sitemaps_url_pattern:
            return self._retrieve_sitemaps_from_root(
                sitemap_url, sitemaps_url_pattern
            )

        return [sitemap_url]

    def _retrieve_sitemaps_from_root(
        self, sitemap_url: str, sitemaps_url_pattern: Optional[str] = None
    ):
        sitemap_urls = []
        try:
            root_sitemap_response = urlopen(sitemap_url)
            soup = BeautifulSoup(root_sitemap_response, self.PARSER)

            sitemap_nodes = soup.find_all("sitemap")

            for node in sitemap_nodes:
                url = node.find("loc").string

                if not sitemaps_url_pattern:
                    sitemap_urls.append(url)
                else:
                    if re.match(sitemaps_url_pattern, url):
                        sitemap_urls.append(url)
        except URLError as error:
            raise PageRetrieverFatalError(str(error))

        return sitemap_urls

    def _retrieve_from_sitemap(self, sitemap_url: str, max_urls: int):
        if 0 < max_urls <= len(self.__urls):
            return

        try:
            sitemap_response = urlopen(sitemap_url)
            soup = BeautifulSoup(sitemap_response, self.PARSER)

            nodes = soup.find_all("url")

            for node in nodes:
                address = str(node.find("loc").string)

                self.__urls[address] = Url(address)

                if 0 < max_urls <= len(self.__urls):
                    break
        except (URLError, InvalidUrlException) as error:
            raise PageRetrieverFatalError(str(error))

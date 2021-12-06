from __future__ import annotations

import os
import re
from typing import Optional, List, Dict
from datetime import datetime
from http import HTTPStatus
from time import sleep
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from json import loads, decoder
import requests
import pytz

import urllib3

from bs4 import BeautifulSoup

import shared.infrastructure.environment.globalvars as glob
from shared.domain.service.caching.cache import Cache
from shared.domain.model.valueobject.url import Url
from corpus.build.domain.service.pagerequester import (
    PageRequester,
    Response,
    Request,
    RetrievalError,
    PageRequesterFatalError,
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PageRequesterImpl(PageRequester):
    _DELAY = 0
    _PARSER = "lxml"
    _STRING_SEPARATOR = " "
    _ACTION_ON_429_STATUS = "retry"  # or 'exit'
    _REQUEST_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,es;q=0.7,ca;q=0.6,"
        "it;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/92.0.4515.107 Safari/537.36",
    }
    _EXCLUDE_REQUEST_HEADERS = ["If-Modified-Since"]
    _DEFAULT_BLACKLISTED_TAGS = [
        "[document]",
        "noscript",
        "header",
        "footer",
        "iframe",
        "html",
        "meta",
        "script",
        "br",
    ]

    def __init__(self, cache: Cache):
        self._cache = cache

    def request(self, request: Request) -> Response:

        if self._DELAY > 0:
            sleep(self._DELAY)

        self._ensure_scraping_is_allowed(request.url)

        headers = self._request_headers(request.headers)
        try:
            last_modified_on = self._last_extracted_date_cached(request.url)

            if last_modified_on:
                headers["If-Modified-Since"] = last_modified_on

            http_response = requests.get(
                request.url.address,
                allow_redirects=True,
                verify=glob.settings.is_production(),
                headers=headers,
            )

            modified_on = _date_to_local(http_response.headers.get("Date"))

            self._ensure_is_a_valid_response(http_response)

            response = Response(
                http_response.status_code,
                http_response.reason,
                modified_on,
                request,
            )

            if http_response.status_code not in [
                HTTPStatus.OK,
                HTTPStatus.NOT_MODIFIED,
            ]:
                return response

            if http_response.history:
                last_response = http_response.history[-1]

                response.status_code = last_response.status_code
                response.status = last_response.reason

                response.final_url = Url(http_response.url)

            if http_response.status_code == HTTPStatus.NOT_MODIFIED:
                return response

            self._cache_last_extracted_date(
                request.url.address,
                http_response.headers.get("Date"),
            )

            markup_parser = MarkupParser(
                self._retrieve_content(http_response.content)
            )

            response.h1 = markup_parser.h1()
            response.title = markup_parser.title()
            response.is_indexable = markup_parser.is_indexable(http_response)
            response.canonical_url = markup_parser.canonical_version()
            response.datalayer = markup_parser.datalayer()

            blacklisted_tags = request.excluded_tags
            blacklisted_tags.extend(self._DEFAULT_BLACKLISTED_TAGS)
            body = markup_parser.body(
                blacklisted_tags, request.excluded_selectors
            )

            selector_mapping = request.selector_mapping
            response.content = self._build_content(body, **selector_mapping)

            return response
        except requests.exceptions.RequestException as error:
            raise RetrievalError(str(error))

    def _build_content(self, body, **selectors):
        page_content = {}

        if selectors:
            for (name, selector) in selectors.items():
                selector_tags = body.select(selector)
                page_content[name] = self._STRING_SEPARATOR.join(
                    [
                        self._STRING_SEPARATOR.join(
                            tag.get_text(
                                self._STRING_SEPARATOR, strip=True
                            ).split()
                        )
                        for tag in selector_tags
                    ]
                )
        else:
            tags = body.find_all()

            page_content["body"] = self._STRING_SEPARATOR.join(
                [
                    self._STRING_SEPARATOR.join(
                        tag.get_text(
                            self._STRING_SEPARATOR, strip=True
                        ).split()
                    )
                    for tag in tags
                ]
            )

        return page_content

    def _ensure_scraping_is_allowed(self, url: Url) -> None:
        url_struct = urlparse(url.address)
        robots_url = "{}://{}/robots.txt".format(
            url_struct.scheme, url_struct.netloc
        )

        robot_parser = RobotFileParser(robots_url)
        robot_parser.read()

        if not robot_parser.can_fetch(
            self._REQUEST_HEADERS.get("User-Agent"), url.address
        ):
            raise RetrievalError("robots.txt forbidden the content")

    def _request_headers(self, request_headers: Dict) -> Dict:
        clean_request_headers = {
            name: value
            for name, value in request_headers.items()
            if name not in self._EXCLUDE_REQUEST_HEADERS
        }

        return {**self._REQUEST_HEADERS, **clean_request_headers}

    def _ensure_is_a_valid_response(self, response):
        if response.status_code != HTTPStatus.TOO_MANY_REQUESTS:
            return

        if self._ACTION_ON_429_STATUS == "exit":
            raise PageRequesterFatalError(
                "The server responded with a status of {} {}".format(
                    response.status_code, response.reason
                )
            )

    def _retrieve_content(self, content: bytes):
        return BeautifulSoup(content, self._PARSER)

    def _last_extracted_date_cached(self, url: Url) -> Optional[str]:
        date = self._cache.read(url.address)
        if not date:
            return None

        return date.decode("utf-8")

    def _cache_last_extracted_date(self, url: str, date: str) -> None:
        self._cache.write(url, date)


def _date_to_local(gmt_date: str):
    date = datetime.strptime(gmt_date, "%a, %d %b %Y %H:%M:%S %Z")
    gmt_timezone = pytz.timezone("GMT")
    date = gmt_timezone.localize(date)

    return date.astimezone(pytz.timezone(os.environ["TZ"]))


class MarkupParser:
    def __init__(self, markup):
        self.markup = markup

    def body(
        self,
        blacklisted_tags: List[str] = None,
        blacklisted_selectors: List[str] = None,
    ):
        try:
            body = self.markup.body

            if blacklisted_tags:
                for tag in body.find_all(name=set(blacklisted_tags)):
                    tag.decompose()

            if not blacklisted_selectors:
                return body

            for blacklisted_selector in set(blacklisted_selectors):
                for selector in body.select(blacklisted_selector):
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
        canonical = self.markup.find("link", attrs={"rel": "canonical"})

        if not canonical:
            return None

        return Url(canonical.attrs["href"])

    def is_indexable(self, response) -> bool:
        if "X-Robots-Tag" not in response.headers:
            meta_robots = self.markup.find("meta", attrs={"name": "robots"})

            if not meta_robots:
                return True

            return "noindex" not in meta_robots.get("content")

        return "noindex" not in response.headers.get("X-Robots-Tag")

    def datalayer(self) -> Dict:
        try:
            script_text = self.markup.find(
                string=re.compile(r"var\s+dataLayer")
            ).split("= ", 1)[1]

            return loads(script_text[: script_text.find("];")] + "]")[0]
        except decoder.JSONDecodeError:
            return {}

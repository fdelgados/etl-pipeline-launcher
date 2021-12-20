from shared.domain.model.valueobject.url import Url, NullUrl
from shared.domain.model.entity.document import Document


class Page(Document):
    def __init__(self, url: Url, content: str, datalayer: dict):
        self._url = url
        self._content = content
        self._datalayer = datalayer

    @property
    def url(self) -> Url:
        return self._url

    @property
    def content(self) -> str:
        return self._content

    @property
    def datalayer(self) -> dict:
        return self._datalayer

    def is_null(self) -> bool:
        return False


class NullPage(Page):
    def __init__(self):
        self._url = NullUrl()
        self._content = ""
        self._datalayer = {}

    def is_null(self) -> bool:
        return True

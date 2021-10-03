from shared.domain.model.value_object.url import Url
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

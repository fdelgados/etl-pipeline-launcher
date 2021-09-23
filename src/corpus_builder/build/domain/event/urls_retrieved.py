from shared.domain.event.event import DomainEvent


class UrlsRetrieved(DomainEvent):
    def __init__(self, tenant_id: str, build_id: str, total_pages: int):
        self._tenant_id = tenant_id
        self._build_id = build_id
        self._total_pages = total_pages

        super().__init__(self._build_id)

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def build_id(self) -> str:
        return self._build_id

    @property
    def total_pages(self):
        return self._total_pages

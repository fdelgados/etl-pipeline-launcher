from shared_context.domain.events import DomainEvent


class ExtractionCompleted(DomainEvent):
    _EVENT_NAME = "extraction_completed"

    def __init__(self, etl_id: str, number_of_urls: int):
        self._number_of_urls = number_of_urls
        self._etl_id = etl_id

        super().__init__(self._etl_id)

    @property
    def number_of_urls(self) -> int:
        return self._number_of_urls

    @property
    def etl_id(self) -> str:
        return self._etl_id

    def event_name(self) -> str:
        return self._EVENT_NAME

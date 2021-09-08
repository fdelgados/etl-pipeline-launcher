from shared.infrastructure.event import DomainEvent


class ExtractionCompleted(DomainEvent):
    def __init__(self, pipeline_id: str, number_of_urls: int):
        self._number_of_urls = number_of_urls

        super().__init__(pipeline_id)

    @property
    def number_of_urls(self) -> int:
        return self._number_of_urls

    @property
    def pipeline_id(self) -> str:
        return self._pipeline_id

    def event_name(self) -> str:
        return 'extraction_completed'

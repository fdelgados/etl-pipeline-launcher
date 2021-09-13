from shared_context.domain.events import DomainEvent


class ExtractionStarted(DomainEvent):
    _EVENT_NAME = "extraction_started"

    def __init__(self, etl_id: str):
        self._etl_id = etl_id

        super().__init__(self._etl_id)

    @property
    def etl_id(self):
        return self._etl_id

    def event_name(self) -> str:
        return self._EVENT_NAME

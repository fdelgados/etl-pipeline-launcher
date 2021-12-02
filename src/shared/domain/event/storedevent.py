from datetime import datetime


class StoredEvent:
    def __init__(
        self,
        event_id: str,
        aggregate_id: str,
        occurred_on: datetime,
        event_data: str,
        event_name: str,
    ):
        self._event_id = event_id
        self._aggregate_id = aggregate_id
        self._occurred_on = occurred_on
        self._event_data = event_data
        self._event_name = event_name

    @property
    def event_id(self) -> str:
        return self._event_id

    @property
    def aggregate_id(self) -> str:
        return self._aggregate_id

    @property
    def occurred_on(self) -> datetime:
        return self._occurred_on

    @property
    def event_data(self) -> str:
        return self._event_data

    @property
    def event_name(self) -> str:
        return self._event_name

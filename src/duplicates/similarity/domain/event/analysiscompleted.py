from shared.domain.bus.event import DomainEvent


class AnalysisCompleted(DomainEvent):
    def __init__(self, report_id: str):
        self._report_id = report_id

        super().__init__(self._report_id)

    @property
    def report_id(self):
        return self._report_id

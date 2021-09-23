from typing import List

from shared.domain.bus.event import DomainEventSubscriber
from duplicates.report.domain.event.report_created import ReportCreated


class TransformDataOnReportCreated(DomainEventSubscriber):
    def subscribed_to(self) -> List:
        return [ReportCreated.type_name()]

    def handle(self, domain_event: ReportCreated) -> None:
        pass

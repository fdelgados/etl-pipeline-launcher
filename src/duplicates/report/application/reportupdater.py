from shared.domain.bus.event import DomainEventSubscriber
from shared.domain.errors.errors import Errors, ApplicationError

from duplicates.data.domain.event.dataloaded import DataLoaded
from duplicates.data.domain.model.transformedpagecontent import TransformedPageContentRepository
from duplicates.report.domain.model.report import ReportRepository, ReportId


class UpdateReportOnDataLoaded(DomainEventSubscriber):
    def __init__(
        self,
        report_repository: ReportRepository,
        transformed_page_content_repository: TransformedPageContentRepository,
    ):
        super().__init__()

        self._report_repository = report_repository
        self._transformed_page_content_repository = transformed_page_content_repository

    def handle(self, domain_event: DataLoaded) -> None:
        report = self._report_repository.report_of_id(ReportId(domain_event.report_id))

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Report", entity_id=domain_event.report_id
                )
            )

        report.total_pages = self._transformed_page_content_repository.size_of_report(report.name)

        self._report_repository.save(report)




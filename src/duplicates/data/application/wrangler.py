from shared.domain.bus.event import DomainEventSubscriber, EventBus
from shared.domain.errors.errors import Errors, ApplicationError
from duplicates.report.domain.event.reportcreated import ReportCreated
from duplicates.data.domain.service.datagatherer import DataGatherer
from duplicates.data.domain.service.datatransformer import DataTransformer
from duplicates.data.domain.event.dataloaded import DataLoaded
from duplicates.report.domain.model.report import ReportRepository, ReportId
from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContentRepository,
)


class WrangleDataOnReportCreated(DomainEventSubscriber):
    def __init__(
        self,
        data_gatherer: DataGatherer,
        data_transformer: DataTransformer,
        transformed_page_content_repository: TransformedPageContentRepository,
        report_repository: ReportRepository,
        event_bus: EventBus,
    ):
        super().__init__()

        self._data_gatherer = data_gatherer
        self._transformed_page_content_repository = (
            transformed_page_content_repository
        )
        self._data_transformer = data_transformer
        self._report_repository = report_repository
        self._event_bus = event_bus

    def handle(self, domain_event: ReportCreated) -> None:
        pages = self._data_gatherer.gather(
            domain_event.from_corpus, domain_event.corpus_build_id
        )
        report = self._report_repository.report_of_id(
            ReportId(domain_event.report_id)
        )

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Report", entity_id=domain_event.report_id
                )
            )

        clean_pages = self._data_transformer.transform(pages)

        self._transformed_page_content_repository.add_all(
            report.tenant_id,
            clean_pages,
        )

        self._event_bus.publish(DataLoaded(report.report_id.value))

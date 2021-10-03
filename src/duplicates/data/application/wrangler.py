from shared.domain.bus.event import DomainEventSubscriber
from shared.domain.errors.errors import Errors, ApplicationError
from duplicates.report.domain.event.report_created import ReportCreated
from duplicates.data.domain.service.datagatherer import DataGatherer
from duplicates.data.domain.service.dataloader import DataLoader
from duplicates.data.domain.service.datatransformer import DataTransformer
from duplicates.report.domain.model.report import ReportRepository, ReportId


class WrangleDataOnReportCreated(DomainEventSubscriber):
    def __init__(
        self,
        data_gatherer: DataGatherer,
        data_transformer: DataTransformer,
        data_loader: DataLoader,
        report_repository: ReportRepository,
    ):
        super().__init__()

        self._data_gatherer = data_gatherer
        self._data_loader = data_loader
        self._data_transformer = data_transformer
        self._report_repository = report_repository

    def handle(self, domain_event: ReportCreated) -> None:
        pages = self._data_gatherer.gather(domain_event.from_corpus)
        report = self._report_repository.report_of_id(ReportId(domain_event.report_id))

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(
                    entity_name="Report", entity_id=domain_event.report_id
                )
            )

        clean_pages = self._data_transformer.transform(pages)

        self._data_loader.load(clean_pages, report)

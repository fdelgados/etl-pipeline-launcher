from shared.domain.bus.event import DomainEventSubscriber
from shared.domain.errors.errors import Errors, ApplicationError
from duplicates.report.domain.event.report_created import ReportCreated
from duplicates.data.domain.model.page import PageRetriever
from duplicates.data.domain.service.dataloader import DataLoader
from duplicates.report.domain.model.report import ReportRepository, ReportId


class TransformDataOnReportCreated(DomainEventSubscriber):
    def __init__(
        self,
        page_retriever: PageRetriever,
        data_loader: DataLoader,
        report_repository: ReportRepository,
    ):
        super().__init__()

        self._page_retriever = page_retriever
        self._data_loader = data_loader
        self._report_repository = report_repository

    def handle(self, domain_event: ReportCreated) -> None:
        pages = self._page_retriever.retrieve_all(domain_event.from_corpus)
        report = self._report_repository.report_of_id(ReportId(domain_event.report_id))

        if not report:
            raise ApplicationError(
                Errors.entity_not_found(entity_name="Report", entity_id=domain_event.report_id)
            )

        self._data_loader.load(pages, report)

import abc
from datetime import datetime

from coolname import generate

from shared_context.domain.model import Uuid, AggregateRoot, Repository
from shared.domain.model.user.user import User
from duplicates.shared.domain.model.similarity_threshold import SimilarityThreshold
from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.report.domain.event.report_created import ReportCreated


class ReportId(Uuid):
    pass


class Report(AggregateRoot):
    def __init__(
        self,
        report_id: ReportId,
        name: str,
        creator: User,
        k_shingle_size: KShingleSize,
        similarity_threshold: SimilarityThreshold,
    ):
        self._id = report_id
        self._name = name
        self._creator = creator
        self._created_by = self._creator.username()
        self._tenant_id = self._creator.tenant_id()
        self._k_shingle_size = k_shingle_size
        self._similarity_threshold = similarity_threshold
        self._completed_on = None
        self._total_pages = 0
        self._duplicated_pages = 0
        self._duplication_ratio = None
        self._duplication_average = None
        self._duplication_median = None
        self._completed = False

        report_created = ReportCreated(
            self._id.value,
            self._name,
            self._created_by,
            self._tenant_id,
            self._k_shingle_size.value,
            self._similarity_threshold.value,
        )

        self._started_on = report_created.occurred_on

        self.record_event(report_created)

    @property
    def id(self) -> ReportId:
        return self._id

    @property
    def created_by(self) -> str:
        return self._created_by

    @property
    def tenant_id(self) -> str:
        return self._tenant_id

    @property
    def creator(self) -> User:
        return self._creator

    @property
    def k_shingle_size(self) -> KShingleSize:
        return self._k_shingle_size

    @property
    def similarity_threshold(self) -> SimilarityThreshold:
        return self._similarity_threshold

    @property
    def started_on(self) -> datetime:
        return self._started_on

    def complete(self):
        self._completed = True
        self._completed_on = datetime.now()

    def is_completed(self) -> bool:
        return self._completed


class ReportRepository(Repository, metaclass=abc.ABCMeta):
    @staticmethod
    def next_identity() -> ReportId:
        return ReportId()

    @staticmethod
    def generate_unique_name() -> str:
        return " ".join(x.capitalize() for x in generate(2))

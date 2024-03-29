import abc

from dataclasses import dataclass

from duplicates.report.domain.model.report import Report


@dataclass(frozen=True)
class ReportStats:
    analyzed_pages: int
    duplicated_pages: int
    similarity_average: float
    similarity_median: float
    duplication_ratio: float


class ReportStatsRetriever(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def retrieve(self, report: Report) -> ReportStats:
        raise NotImplementedError

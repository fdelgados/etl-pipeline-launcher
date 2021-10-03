import abc

from typing import List

from duplicates.data.domain.model.cleanpage import CleanPageContent
from duplicates.report.domain.model.report import Report


class DataLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, data: List[CleanPageContent], report: Report) -> None:
        raise NotImplementedError

import abc

from typing import List

from duplicates.data.domain.model.page import Page
from duplicates.report.domain.model.report import Report


class DataLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, data: List[Page], report: Report) -> None:
        raise NotImplementedError

import abc

from duplicates.report.domain.model.report import Report


class SimilarityCalculator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calculate(self, report: Report):
        raise NotImplementedError

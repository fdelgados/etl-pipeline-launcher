import abc

from typing import List

from duplicates.data.domain.model.cleanpage import CleanPageContent
from duplicates.data.domain.model.page import Page


class DataTransformer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def transform(self, data: List[Page]) -> List[CleanPageContent]:
        raise NotImplementedError

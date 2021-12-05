import abc

from typing import List

from duplicates.data.domain.model.page import Page


class DataGatherer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def gather(self, corpus: str, corpus_build_id: str) -> List[Page]:
        raise NotImplementedError

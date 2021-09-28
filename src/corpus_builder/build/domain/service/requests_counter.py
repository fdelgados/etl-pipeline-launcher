import abc

from corpus_builder.build.domain.model.build import BuildId


class RequestsCounter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def count_successful(self, build_id: BuildId) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def count_failed(self, build_id: BuildId) -> int:
        raise NotImplementedError

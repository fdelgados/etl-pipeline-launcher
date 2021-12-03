import abc

from corpus.build.domain.model.build import BuildId, Build


class RequestsCounter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def count_successful(self, build: Build) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def count_failed(self, build_id: BuildId) -> int:
        raise NotImplementedError

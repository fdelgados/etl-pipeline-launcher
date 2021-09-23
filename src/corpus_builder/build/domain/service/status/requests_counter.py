import abc

from corpus_builder.build.domain.model.build import BuildId


class RequestsCounter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def count(self, build_id: BuildId):
        raise NotImplementedError

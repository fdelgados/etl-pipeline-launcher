import abc


class CorpusManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def rotate(self, corpus: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clean(self, corpus: str) -> None:
        raise NotImplementedError

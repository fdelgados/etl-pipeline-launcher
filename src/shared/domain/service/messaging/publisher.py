import abc


class Publisher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def publish(self, message: str, exchange: str = '') -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _connect(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _disconnect(self):
        raise NotImplementedError

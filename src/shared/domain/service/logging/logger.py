import abc


class Logger(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not Logger:
            return NotImplementedError

        if not hasattr(subclass, 'debug') or not callable(subclass.debug):
            return NotImplementedError

        if not hasattr(subclass, 'info') or not callable(subclass.info):
            return NotImplementedError

        if not hasattr(subclass, 'warning') or not callable(subclass.warning):
            return NotImplementedError

        if not hasattr(subclass, 'error') or not callable(subclass.error):
            return NotImplementedError

        if not hasattr(subclass, 'critical') or not callable(subclass.critical):
            return NotImplementedError

    @abc.abstractmethod
    def debug(self, message: str, *args) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def info(self, message: str, *args) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def warning(self, message: str, *args) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def error(self, message: str, *args) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def critical(self, message: str) -> None:
        raise NotImplementedError

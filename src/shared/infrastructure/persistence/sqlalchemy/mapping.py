import abc

from sqlalchemy import MetaData, create_engine


class Mapping(metaclass=abc.ABCMeta):
    def map_entities(self, dsn: str) -> None:
        metadata = MetaData()
        metadata.reflect(create_engine(dsn))

        self._do_mapping(metadata)

    @abc.abstractmethod
    def _do_mapping(self, metadata: MetaData) -> None:
        raise NotImplementedError

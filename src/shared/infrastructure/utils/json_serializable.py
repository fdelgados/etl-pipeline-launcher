import abc

from typing import Union


class JsonSerializable(metaclass=abc.ABCMeta):
    def serialize(self) -> Union[dict, list]:
        return self.__dict__

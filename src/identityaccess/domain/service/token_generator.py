import abc

from identityaccess.domain.model.user import UserDescriptor


class TokenGenerator(metaclass=abc.ABCMeta):
    TOKEN_TYPE = ""

    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not TokenGenerator:
            return NotImplementedError

        if not hasattr(subclass, "generate") or not callable(subclass.generate):
            return NotImplementedError

        return True

    @abc.abstractmethod
    def generate(self, user: UserDescriptor) -> str:
        raise NotImplementedError

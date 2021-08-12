import abc

from identityaccess.domain.model.scope import Scope


class AuthorizationError(RuntimeError):
    pass


class AuthorizationService(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not AuthorizationService:
            return NotImplementedError

        if not hasattr(subclass, "authorize") or not callable(subclass.authorize):
            return NotImplementedError

        return True

    @abc.abstractmethod
    def authorize(self, access_token: str, scope: Scope) -> None:
        raise NotImplementedError

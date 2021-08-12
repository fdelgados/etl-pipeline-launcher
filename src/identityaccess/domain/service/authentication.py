import abc

from identityaccess.domain.model.user import UserDescriptor
from identityaccess.domain.model.tenant import TenantId
from identityaccess import IdentityAccessError


class AuthenticationError(IdentityAccessError):
    pass


class AuthenticationService(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not AuthenticationService:
            return NotImplementedError

        if not hasattr(subclass, "authenticate") or not callable(subclass.authenticate):
            return NotImplementedError

        return True

    @abc.abstractmethod
    def authenticate(self, tenant_id: TenantId, username: str, password: str) -> UserDescriptor:
        raise NotImplementedError

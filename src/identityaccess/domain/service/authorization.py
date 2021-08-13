import abc

from identityaccess.domain.model.scope import Scope
from identityaccess.domain.model.tenant import TenantId
from identityaccess.domain.model.access_token import AccessToken
from identityaccess import IdentityAccessError


class AuthorizationError(IdentityAccessError):
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
    def authorize(self, tenant_id: TenantId, access_token: AccessToken, scope: Scope) -> None:
        raise NotImplementedError

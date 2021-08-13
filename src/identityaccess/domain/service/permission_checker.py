import abc

from identityaccess import IdentityAccessError

from identityaccess.domain.model.tenant import TenantId
from identityaccess.domain.model.role import Role
from identityaccess.domain.model.scope import Scope


class PermissionDeniedError(IdentityAccessError):
    pass


class PermissionChecker(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not PermissionChecker:
            return NotImplementedError

        if not hasattr(subclass, 'check') or not callable(subclass.check):
            return NotImplementedError

        return True

    @abc.abstractmethod
    def check(self, tenant_id: TenantId, role: Role, scope: Scope) -> None:
        raise NotImplementedError

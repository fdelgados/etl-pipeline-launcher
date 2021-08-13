from .tenant import TenantId

import abc
from shared_context.domain.model import Repository, AggregateRoot


class Permission(AggregateRoot):
    def __init__(self, tenant_id: TenantId, role: str, scope: str):
        self.tenant_id = tenant_id
        self.role = role
        self.scope = scope


class PermissionRepository(Repository, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not PermissionRepository:
            return NotImplementedError

        if not hasattr(subclass, 'is_allowed_for') or not callable(subclass.is_allowed_for):
            return NotImplementedError

    @abc.abstractmethod
    def is_allowed_for(self, tenant_id: TenantId, role: str, scope: str) -> bool:
        raise NotImplementedError

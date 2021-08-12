import abc
from shared_context.domain.model import Uuid, Repository, AggregateRoot


class TenantId(Uuid):
    pass


class Tenant(AggregateRoot):
    def __init__(self, id: TenantId, company_name: str, is_active: bool):
        self.id = id
        self.company_name = company_name
        self.is_active = is_active
        self.scopes = {
            "foo": ["admin"]
        }

    def can(self, role: str, scope: str) -> bool:
        roles_by_scope = self.scopes.get(scope)

        if not roles_by_scope:
            return False

        return role in roles_by_scope


class TenantRepository(Repository, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        if subclass is not TenantRepository:
            return NotImplementedError

        if not hasattr(subclass, "tenant_of_id") or not callable(subclass.tenant_of_id):
            return NotImplementedError

    @abc.abstractmethod
    def tenant_of_id(self, tenant_id: TenantId) -> Tenant:
        raise NotImplementedError

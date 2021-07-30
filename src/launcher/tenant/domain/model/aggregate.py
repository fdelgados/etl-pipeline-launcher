from shared_context.domain.model import AggregateRoot
from shared_context.domain.model import Uuid


class TenantId(Uuid):
    pass


class Tenant(AggregateRoot):
    def __init__(self, id: TenantId, company_name: str, is_active: bool):
        self.id = id
        self.company_name = company_name
        self.is_active = is_active

from shared_context.domain.service import Finder
from launcher.tenant.domain.model.aggregate import Tenant, TenantId
from launcher.tenant.domain.model.repository import TenantRepository
from launcher.tenant.domain.errors import TenantNotFoundException


class TenantFinder(Finder):
    def __init__(self, tenant_repository: TenantRepository):
        self.__tenant_repository = tenant_repository

    def find(self, tenant_id: TenantId) -> Tenant:
        tenant = self.__tenant_repository.find(id=tenant_id)
        if not tenant:
            raise TenantNotFoundException("Tenant with tenant_id {} not found".format(tenant_id))

        return tenant

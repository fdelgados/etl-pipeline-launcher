from shared_context.infrastructure.persistence.sqlalchemy import Repository
from launcher.tenant.domain.model.repository import TenantRepository
from launcher.tenant.domain.model.aggregate import Tenant
from shared.infrastructure.application.settings import Settings


class SqlAlchemyTenantRepository(TenantRepository, Repository):
    def __init__(self):
        super().__init__(Tenant, Settings.database_dsn())

from typing import Optional

from shared_context.infrastructure.persistence.sqlalchemy import Repository
from identityaccess.domain.model.tenant import Tenant, TenantRepository, TenantId
from identityaccess.domain.model.user import User, UserRepository
from identityaccess.domain.model.permission import Permission, PermissionRepository
from shared.infrastructure.application.settings import Settings


class SqlAlchemyTenantRepository(TenantRepository, Repository):
    def __init__(self):
        super().__init__(Tenant, Settings.database_dsn("identityaccess"))

    def tenant_of_id(self, tenant_id: TenantId) -> Optional[Tenant]:
        return self.find(id=tenant_id)


class SqlAlchemyUserRepository(UserRepository, Repository):
    def __init__(self):
        super().__init__(User, Settings.database_dsn("identityaccess"))

    def user_from_credentials(self, tenant_id: TenantId, username: str, password: str) -> Optional[User]:
        return self.find(tenant_id=tenant_id, username=username, password=password)


class SqlAlchemyPermissionRepository(PermissionRepository, Repository):
    def __init__(self):
        super().__init__(Permission, Settings.database_dsn("identityaccess"))

    def is_allowed_for(self, tenant_id: TenantId, role: str, scope: str) -> bool:
        permission = self.find(tenant_id=tenant_id, role=role, scope=scope)

        return permission is not None

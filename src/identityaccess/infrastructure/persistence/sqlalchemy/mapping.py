from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    String,
    Boolean
)
from sqlalchemy.orm import registry

from identityaccess.domain.model.tenant import Tenant
from identityaccess.domain.model.user import User
from identityaccess.domain.model.role import Role
from identityaccess.domain.model.scope import Scope
from identityaccess.domain.model.permission import Permission
from identityaccess.infrastructure.persistence.sqlalchemy.type import TenantIdType
from shared_context.infrastructure.persistence.sqlalchemy import Orm


class IdentityAccessOrm(Orm):
    def start_mappers(self) -> None:

        mapper_registry = registry()

        tenants_table = Table(
            "tenants",
            mapper_registry.metadata,
            Column("id", TenantIdType, primary_key=True),
            Column("company_name", String(100), nullable=False),
            Column("active", Boolean, nullable=False)
        )

        mapper_registry.map_imperatively(
            Tenant,
            tenants_table,
            properties={
                "is_active": tenants_table.c.active
            }
        )

        users_table = Table(
            "users",
            mapper_registry.metadata,
            Column("tenant_id", TenantIdType, ForeignKey('tenants.id'), primary_key=True),
            Column("username", String(30), primary_key=True),
            Column("email", String(100), nullable=False),
            Column("password", String(40)),
            Column("first_name", String(50), nullable=True),
            Column("last_name", String(100), nullable=True),
            Column("is_enabled", Boolean, nullable=False),
            Column("role", String(30), nullable=False)
        )

        mapper_registry.map_imperatively(User, users_table)

        roles_table = Table(
            "roles",
            mapper_registry.metadata,
            Column("name", String, primary_key=True),
            Column("description", String, nullable=True)
        )

        mapper_registry.map_imperatively(Role, roles_table)

        scopes_table = Table(
            "scopes",
            mapper_registry.metadata,
            Column("name", String, primary_key=True),
            Column("description", String, nullable=True)
        )

        mapper_registry.map_imperatively(Scope, scopes_table)

        permissions_table = Table(
            'permissions',
            mapper_registry.metadata,
            Column("tenant_id", TenantIdType, ForeignKey('tenants.id'), primary_key=True),
            Column('role_name', String(30), ForeignKey('roles.name'), primary_key=True),
            Column('scope_name', String(30), ForeignKey('scopes.name'), primary_key=True)
        )

        mapper_registry.map_imperatively(
            Permission,
            permissions_table,
            properties={
                'role': permissions_table.c.role_name,
                'scope': permissions_table.c.scope_name,
            }
        )

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
from identityaccess.infrastructure.persistence.sqlalchemy.type import TenantIdType
from shared_context.infrastructure.persistence.sqlalchemy import Orm


class IdentityAccessOrm(Orm):
    def start_mappers(self) -> None:

        mapper_registry = registry()

        tenants = Table(
            "tenants",
            mapper_registry.metadata,
            Column("id", TenantIdType, primary_key=True),
            Column("company_name", String(100), nullable=False),
            Column("active", Boolean, nullable=False)
        )

        mapper_registry.map_imperatively(
            Tenant,
            tenants,
            properties={
                "is_active": tenants.c.active
            }
        )

        users = Table(
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

        mapper_registry.map_imperatively(User, users)

        roles = Table(
            "roles",
            mapper_registry.metadata,
            Column("name", String, primary_key=True),
            Column("description", String, nullable=True)
        )

        mapper_registry.map_imperatively(Role, roles)

        scopes = Table(
            "scopes",
            mapper_registry.metadata,
            Column("name", String, primary_key=True),
            Column("description", String, nullable=True)
        )

        mapper_registry.map_imperatively(Scope, scopes)

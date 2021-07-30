from sqlalchemy import (
    Table,
    MetaData,
    Column,
    String,
    Boolean
)
from sqlalchemy.orm import mapper

from shared_context.infrastructure.persistence.sqlalchemy import Orm

from launcher.tenant.domain.model.aggregate import Tenant
from launcher.tenant.infrastructure.persistence.sqlalchemy.type import TenantIdType


class LauncherOrm(Orm):
    def start_mappers(self) -> None:
        metadata = MetaData()

        tenants = Table(
            "tenants",
            metadata,
            Column("id", TenantIdType, primary_key=True),
            Column("company_name", String(100), nullable=False),
            Column("active", Boolean, nullable=False)
        )

        mapper(
            Tenant,
            tenants,
            properties={
                "is_active": tenants.c.active
            }
        )

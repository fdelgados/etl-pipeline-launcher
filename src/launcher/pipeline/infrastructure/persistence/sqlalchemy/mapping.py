from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Boolean
)
from sqlalchemy.orm import mapper

from shared_context.infrastructure.persistence.sqlalchemy import Orm

from launcher.pipeline.domain.model.aggregate import Pipeline
from launcher.pipeline.infrastructure.persistence.sqlalchemy.type import PipelineIdType
from launcher.tenant.infrastructure.persistence.sqlalchemy.type import TenantIdType


class LauncherOrm(Orm):
    def start_mappers(self) -> None:
        metadata = MetaData()

        pipelines = Table(
            "pipelines",
            metadata,
            Column("id", PipelineIdType, primary_key=True),
            Column("tenant_id", TenantIdType, nullable=False),
            Column("completed", Boolean, nullable=False, default=False)
        )

        mapper(
            Pipeline,
            pipelines,
            properties={
                "pipeline_id": pipelines.c.id
            }
        )

from sqlalchemy import (
    Table,
    String,
    MetaData,
    Column,
    Boolean
)
from sqlalchemy.orm import mapper

from shared_context.infrastructure.persistence.sqlalchemy import Orm

from launcher.pipeline.domain.model import Pipeline
from launcher.pipeline.infrastructure.persistence.sqlalchemy.type import PipelineIdType


class LauncherMapping(Orm):
    def start_mappers(self) -> None:
        metadata = MetaData()

        pipelines = Table(
            "pipelines",
            metadata,
            Column("id", PipelineIdType, primary_key=True),
            Column("tenant_id", String(36), nullable=False),
            Column("launched_by", String(30), nullable=False),
            Column("completed", Boolean, nullable=False, default=False)
        )

        mapper(
            Pipeline,
            pipelines,
            properties={
                "pipeline_id": pipelines.c.id
            }
        )

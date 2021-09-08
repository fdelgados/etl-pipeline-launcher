from typing import Optional
from shared_context.infrastructure.persistence.sqlalchemy import Repository
from launcher.pipeline.domain.model.pipeline import (
    PipelineRepository,
    Pipeline,
    PipelineId
)

from shared import settings


class PipelineRepositoryImpl(PipelineRepository, Repository):
    def __init__(self):
        super().__init__(Pipeline, settings.database_dsn('launcher'))

    def pipeline_of_tenant_and_id(self, tenant_id: str, pipeline_id: PipelineId) -> Optional[Pipeline]:
        return self.find(_tenant_id=tenant_id, _pipeline_id=pipeline_id)

from shared_context.infrastructure.persistence.sqlalchemy import Repository
from launcher.pipeline.domain.model.repository import PipelineRepository
from launcher.pipeline.domain.model.aggregate import Pipeline
from shared.infrastructure.application.settings import Settings


class SqlAlchemyPipelineRepository(PipelineRepository, Repository):
    def __init__(self):
        dsn = Settings.database_dsn()
        super().__init__(Pipeline, dsn)

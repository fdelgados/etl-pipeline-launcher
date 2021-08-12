from shared_context.infrastructure.persistence.sqlalchemy import Repository
from launcher.pipeline.domain.model.repository import PipelineRepository
from launcher.pipeline.domain.model.aggregate import Pipeline
from shared.infrastructure.application.settings import Settings


class SqlAlchemyPipelineRepository(PipelineRepository, Repository):
    def __init__(self):
        super().__init__(Pipeline, Settings.database_dsn("launcher"))

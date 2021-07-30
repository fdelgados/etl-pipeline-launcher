from abc import ABC
from shared_context.domain.model import Repository
from launcher.pipeline.domain.model.aggregate import PipelineId


class PipelineRepository(Repository, ABC):
    def generate_identifier(self):
        return PipelineId()

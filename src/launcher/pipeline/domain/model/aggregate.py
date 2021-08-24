from shared_context.domain.model import AggregateRoot
from shared_context.domain.model import Uuid


class PipelineId(Uuid):
    pass


class Pipeline(AggregateRoot):
    def __init__(self, pipeline_id: PipelineId, tenant_id: str, launched_by: str):
        self.pipeline_id = pipeline_id
        self.tenant_id = tenant_id
        self.launched_by = launched_by
        self.completed = False

    def complete(self):
        self.completed = True

    def __repr__(self):
        return 'Pipeline <{}>'.format(self.pipeline_id.value)

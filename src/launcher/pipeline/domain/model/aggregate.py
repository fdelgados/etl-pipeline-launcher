from shared_context.domain.model import AggregateRoot
from shared_context.domain.model import Uuid
from launcher.tenant.domain.model.aggregate import TenantId


class PipelineId(Uuid):
    pass


class Pipeline(AggregateRoot):
    def __init__(self, pipeline_id: PipelineId, tenant_id: TenantId):
        self.pipeline_id = pipeline_id
        self.tenant_id = tenant_id
        self.completed = False

    def complete(self):
        self.completed = True

    def __repr__(self):
        return 'Pipeline <{}>'.format(self.pipeline_id.value)

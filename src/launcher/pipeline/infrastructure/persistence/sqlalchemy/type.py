import uuid

import sqlalchemy.types as types

from launcher.pipeline.domain.model.aggregate import PipelineId


class PipelineIdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.BINARY(16)

    def process_bind_param(self, pipeline_id, dialect):
        return uuid.UUID(pipeline_id.value).bytes

    def process_result_value(self, value, dialect):
        return PipelineId(str(uuid.UUID(bytes=value)))

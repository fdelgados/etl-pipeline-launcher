import uuid

from sqlalchemy import types

from corpus.build.domain.model.build import BuildId, Status


class BuildIdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.BINARY(16)
    cache_ok = True

    def process_bind_param(self, build_id, dialect):
        return uuid.UUID(build_id.value).bytes

    def process_result_value(self, value, dialect):
        return BuildId(str(uuid.UUID(bytes=value)))


class BuildStatusType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.INTEGER

    def process_bind_param(self, build_status, dialect):
        return build_status.value

    def process_result_value(self, value, dialect):
        return Status(value)

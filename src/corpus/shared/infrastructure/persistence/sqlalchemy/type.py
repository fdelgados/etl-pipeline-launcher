import uuid

import sqlalchemy.types as types

from corpus.etl.domain.model.etl import EtlId


class EtlIdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.BINARY(16)
    cache_ok = True

    def process_bind_param(self, etl_id, dialect):
        return uuid.UUID(etl_id.value).bytes

    def process_result_value(self, value, dialect):
        return EtlId(str(uuid.UUID(bytes=value)))

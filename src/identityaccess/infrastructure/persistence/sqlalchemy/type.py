import uuid

import sqlalchemy.types as types

from identityaccess.domain.model.tenant import TenantId


class TenantIdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.BINARY(16)

    def process_bind_param(self, tenant_id, dialect):
        return uuid.UUID(tenant_id.value).bytes

    def process_result_value(self, value, dialect):
        return TenantId(str(uuid.UUID(bytes=value)))

import uuid

import json
import sqlalchemy.types as types
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from launcher.pipeline.domain.model.pipeline import PipelineId
from launcher.pipeline.domain.model.url import Url


class PipelineIdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.BINARY(16)
    cache_ok = True

    def process_bind_param(self, pipeline_id, dialect):
        return uuid.UUID(pipeline_id.value).bytes

    def process_result_value(self, value, dialect):
        return PipelineId(str(uuid.UUID(bytes=value)))


class UrlType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.STRINGTYPE

    def process_bind_param(self, url, dialect):
        return None if url is None else url.address

    def process_result_value(self, value, dialect):
        return None if not value else Url(value)


class UrlIdentityType(UrlType):
    def process_bind_param(self, url, dialect):
        return url.address

    def process_result_value(self, value, dialect):
        return Url(value)


class SerializedText(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        if not value:
            return None

        return json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        if not value:
            return None

        return json.loads(value)

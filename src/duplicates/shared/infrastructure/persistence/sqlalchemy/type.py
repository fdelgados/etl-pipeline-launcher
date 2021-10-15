import uuid

from sqlalchemy import types

from duplicates.report.domain.model.report import ReportId
from duplicates.shared.domain.model.k_shingle_size import KShingleSize
from duplicates.shared.domain.model.similarity_threshold import SimilarityThreshold
from shared.domain.model.valueobject.url import Url


class ReportIdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.BINARY(16)
    cache_ok = True

    def process_bind_param(self, report_id, dialect):
        return uuid.UUID(report_id.value).bytes

    def process_result_value(self, value, dialect):
        return ReportId(str(uuid.UUID(bytes=value)))


class KShingleSizeType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.INTEGER

    def process_bind_param(self, k_shingle_size, dialect):
        return int(k_shingle_size)

    def process_result_value(self, value, dialect):
        return KShingleSize(int(value))


class SimilarityThresholdType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.FLOAT

    def process_bind_param(self, similarity_threshold, dialect):
        return float(similarity_threshold)

    def process_result_value(self, value, dialect):
        return SimilarityThreshold(float(value))


class UrlType(types.TypeDecorator):
    def process_literal_param(self, value, dialect):
        pass

    impl = types.STRINGTYPE
    cache_ok = True

    def process_bind_param(self, url, dialect):
        return url.address

    def process_result_value(self, value, dialect):
        return Url(value)

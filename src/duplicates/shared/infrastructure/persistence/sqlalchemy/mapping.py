from sqlalchemy import Table, String, Column, Boolean, DateTime, Integer, Float

from sqlalchemy.orm import registry

from shared.infrastructure.persistence.sqlalchemy.mapping import Mapping

from duplicates.report.domain.model.report import Report
from duplicates.shared.infrastructure.persistence.sqlalchemy.type import (
    ReportIdType,
    KShingleSizeType,
    SimilarityThresholdType,
)


class DuplicatesMapping(Mapping):
    def map_entities(self) -> None:
        mapper_registry = registry()

        reports_table = Table(
            "reports",
            mapper_registry.metadata,
            Column("id", ReportIdType, primary_key=True),
            Column("tenant_id", String(36), nullable=False),
            Column("created_by", String(60), nullable=False),
            Column("name", String(60), nullable=False),
            Column("completed", Boolean, nullable=False, default=False),
            Column("k_shingle_size", KShingleSizeType, nullable=False),
            Column("similarity_threshold", SimilarityThresholdType, nullable=False),
            Column("started_on", DateTime, nullable=False),
            Column("completed_on", DateTime, nullable=True),
            Column("total_pages", Integer, nullable=False, default=0),
            Column("duplicated_pages", Integer, nullable=False, default=0),
            Column("duplication_ratio", Float, nullable=True),
            Column("duplication_average", Float, nullable=True),
            Column("duplication_median", Float, nullable=True),
        )

        mapper_registry.map_imperatively(
            Report,
            reports_table,
            column_prefix="_",
            properties={"_id": reports_table.c.id},
        )

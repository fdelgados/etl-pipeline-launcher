from sqlalchemy import (
    Table,
    String,
    Column,
    DateTime,
    Integer,
    Float,
)

from sqlalchemy.orm import registry

from shared.infrastructure.persistence.sqlalchemy.mapping import Mapping

from duplicates.report.domain.model.report import Report, Status, Duplicate
from duplicates.check.domain.model.duplicitycheck import DuplicityCheck
from duplicates.check.domain.model.duplicate import (
    Duplicate as DuplicityCheckDuplicate,
)
from duplicates.shared.infrastructure.persistence.sqlalchemy.type import (
    ReportIdType,
    ReportStatusType,
    KShingleSizeType,
    SimilarityThresholdType,
    UrlType,
    DuplicityCheckIdType,
    DuplicityCheckStatusType,
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
            Column("from_corpus", String(25), nullable=False),
            Column("corpus_build_id", String(36), nullable=False),
            Column("corpus_version", String(14), nullable=False),
            Column(
                "status",
                ReportStatusType,
                nullable=False,
                default=Status.created().value,
            ),
            Column("k_shingle_size", KShingleSizeType, nullable=False),
            Column(
                "similarity_threshold", SimilarityThresholdType, nullable=False
            ),
            Column("started_on", DateTime, nullable=False),
            Column("completed_on", DateTime, nullable=True),
            Column("total_pages", Integer, nullable=False, default=0),
            Column("duplicated_pages", Integer, nullable=False, default=0),
            Column("duplication_ratio", Float, nullable=True),
            Column("duplication_average", Float, nullable=True),
            Column("duplication_median", Float, nullable=True),
            extend_existing=True,
        )

        mapper_registry.map_imperatively(
            Report,
            reports_table,
            column_prefix="_",
            properties={"_report_id": reports_table.c.id},
        )

        duplicates_table = Table(
            "report_duplicates",
            mapper_registry.metadata,
            Column("report_id", ReportIdType, primary_key=True),
            Column("url", UrlType, primary_key=True),
            Column("duplicate_url", UrlType, primary_key=True),
            Column("similarity", Float, nullable=False),
            extend_existing=True,
        )

        mapper_registry.map_imperatively(
            Duplicate,
            duplicates_table,
            column_prefix="_",
            properties={
                "_a_url": duplicates_table.c.url,
                "_another_url": duplicates_table.c.duplicate_url,
            },
        )

        duplicity_checks_table = Table(
            "duplicity_checks",
            mapper_registry.metadata,
            Column("id", DuplicityCheckIdType, primary_key=True),
            Column("tenant_id", String(36), nullable=False),
            Column("requested_by", String(30), nullable=False),
            Column("corpus", String(25), nullable=False),
            Column("status", DuplicityCheckStatusType, nullable=False),
            Column(
                "similarity_threshold",
                SimilarityThresholdType,
                nullable=False,
            ),
            Column("requested_on", DateTime, nullable=False),
            Column("completed_on", DateTime, nullable=True),
        )

        mapper_registry.map_imperatively(
            DuplicityCheck,
            duplicity_checks_table,
            column_prefix="_",
        )

        check_duplicates_table = Table(
            "duplicity_check_duplicates",
            mapper_registry.metadata,
            Column(
                "duplicity_check_id",
                DuplicityCheckIdType,
                primary_key=True,
            ),
            Column("url", UrlType, primary_key=True),
            Column("duplicate_url", UrlType, primary_key=True),
            Column("similarity", Float, nullable=False),
            Column("checked_on", DateTime, nullable=False),
            extend_existing=True,
        )

        mapper_registry.map_imperatively(
            DuplicityCheckDuplicate,
            check_duplicates_table,
            column_prefix="_",
            properties={
                "_check_id": check_duplicates_table.c.duplicity_check_id,
                "_a_url": check_duplicates_table.c.url,
                "_another_url": check_duplicates_table.c.duplicate_url,
            },
        )

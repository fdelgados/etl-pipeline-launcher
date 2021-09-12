from sqlalchemy import Table, String, Column, Boolean, DateTime, JSON

from sqlalchemy.orm import registry

from shared_context.infrastructure.persistence.sqlalchemy import Orm

from corpus.etl.domain.model.etl import Etl
from corpus.shared.infrastructure.persistence.sqlalchemy.type import EtlIdType


class CorpusMapping(Orm):
    def start_mappers(self) -> None:

        mapper_registry = registry()

        etl_table = Table(
            "etls",
            mapper_registry.metadata,
            Column("id", EtlIdType, primary_key=True),
            Column("tenant_id", String(36), nullable=False),
            Column("name", String(60), nullable=False),
            Column("launched_by", String(30), nullable=False),
            Column("sitemaps", JSON, nullable=False),
            Column("description", String(200), nullable=True),
            Column("request_headers", JSON, nullable=True),
            Column("selector_mapping", JSON, nullable=True),
            Column("excluded_tags", JSON, nullable=True),
            Column("excluded_selectors", JSON, nullable=True),
            Column("url_address_pattern", String(255), nullable=True),
            Column("custom_request_fields", JSON, nullable=True),
            Column("completed", Boolean, nullable=False, default=False),
            Column("started_on", DateTime, nullable=False),
            Column("completed_on", DateTime, nullable=True),
        )

        mapper_registry.map_imperatively(
            Etl, etl_table, column_prefix="_", properties={"_etl_id": etl_table.c.id}
        )

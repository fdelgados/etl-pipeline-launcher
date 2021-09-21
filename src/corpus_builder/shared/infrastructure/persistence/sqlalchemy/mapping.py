from sqlalchemy import Table, String, Column, Boolean, DateTime, Integer, JSON

from sqlalchemy.orm import registry

from shared_context.infrastructure.persistence.sqlalchemy import Orm

from corpus_builder.build.domain.model.build import Build
from corpus_builder.corpus.domain.model.corpus import Corpus
from corpus_builder.shared.infrastructure.persistence.sqlalchemy.type import BuildIdType


class CorpusBuilderMapping(Orm):
    def start_mappers(self) -> None:

        mapper_registry = registry()

        build_table = Table(
            "builds",
            mapper_registry.metadata,
            Column("id", BuildIdType, primary_key=True),
            Column("tenant_id", String(36), nullable=False),
            Column("name", String(60), nullable=False),
            Column("started_by", String(30), nullable=False),
            Column("corpus_name", String(25), nullable=False),
            Column("total_pages", Integer, nullable=False, default=0),
            Column("completed", Boolean, nullable=False, default=False),
            Column("started_on", DateTime, nullable=False),
            Column("completed_on", DateTime, nullable=True),
        )

        mapper_registry.map_imperatively(
            Build, build_table, column_prefix="_", properties={"_build_id": build_table.c.id}
        )

        corpus_table = Table(
            "corpora",
            mapper_registry.metadata,
            Column("name", String(25), primary_key=True),
            Column("tenant_id", String(36), nullable=False),
            Column("description", String(120), nullable=True),
            Column("sitemaps", JSON, nullable=False),
            Column("request_headers", JSON, nullable=True),
            Column("selector_mapping", JSON, nullable=True),
            Column("excluded_tags", JSON, nullable=True),
            Column("excluded_selectors", JSON, nullable=True),
            Column("url_address_pattern", String(150), nullable=True),
            Column("custom_request_fields", JSON, nullable=True),
        )

        mapper_registry.map_imperatively(
            Corpus, corpus_table, column_prefix="_"
        )

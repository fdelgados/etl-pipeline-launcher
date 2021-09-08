from sqlalchemy import (
    Table,
    String,
    Integer,
    Column,
    Boolean,
    DateTime,
    JSON
)

from sqlalchemy.orm import registry

from shared_context.infrastructure.persistence.sqlalchemy import Orm

from launcher.pipeline.domain.model.pipeline import Pipeline
from launcher.pipeline.domain.model.document import Page
from launcher.pipeline.infrastructure.persistence.sqlalchemy.type import (
    PipelineIdType,
    UrlType,
    UrlIdentityType,
    SerializedText
)


class LauncherMapping(Orm):
    def start_mappers(self) -> None:

        mapper_registry = registry()

        pipelines = Table(
            'pipelines',
            mapper_registry.metadata,
            Column('id', PipelineIdType, primary_key=True),
            Column('tenant_id', String(36), nullable=False),
            Column('name', String(60), nullable=False),
            Column('launched_by', String(30), nullable=False),
            Column('sitemaps_urls', JSON, nullable=False),
            Column('description', String(200), nullable=True),
            Column('request_headers', JSON, nullable=True),
            Column('selector_mapping', JSON, nullable=True),
            Column('excluded_tags', JSON, nullable=True),
            Column('excluded_selectors', JSON, nullable=True),
            Column('url_address_pattern', String(255), nullable=True),
            Column('custom_request_fields', JSON, nullable=True),
            Column('completed', Boolean, nullable=False, default=False),
            Column('started_on', DateTime, nullable=False),
            Column('completed_on', DateTime, nullable=True)
        )

        mapper_registry.map_imperatively(
            Pipeline,
            pipelines,
            column_prefix='_',
            properties={
                '_pipeline_id': pipelines.c.id
            }
        )

        pages = Table(
            'web_corpus',
            mapper_registry.metadata,
            Column('address', UrlIdentityType, primary_key=True),
            Column('status_code', Integer, nullable=False),
            Column('status', String(50), nullable=False),
            Column('h1', String(255), nullable=True),
            Column('title', String(255), nullable=True),
            Column('content', SerializedText, nullable=True),
            Column('is_indexable', Boolean, nullable=True),
            Column('final_address', UrlType, nullable=True),
            Column('canonical_address', UrlType, nullable=True),
            Column('datalayer', SerializedText, nullable=True),
            Column('modified_on', DateTime, nullable=False)
        )

        mapper_registry.map_imperatively(
            Page,
            pages,
            column_prefix='_',
            properties={
                '_url': pages.c.address,
                '_final_url': pages.c.final_address,
                '_canonical_url': pages.c.canonical_address
            }
        )

from typing import Optional, List, Dict
import redis
import json

from shared import settings

from corpus_builder.corpus.domain.model.corpus import Corpus, CorpusRepository


def _to_dict(config: Corpus) -> Dict:
    properties = {}

    for property_name, value in config.__dict__.items():
        if value is None:
            continue
        properties[property_name.lstrip('_')] = value

    return properties


class CorpusRepositoryImpl(CorpusRepository):
    def __init__(self):
        self.client = redis.Redis(
            host=settings.redis_host(),
            port=settings.redis_port(),
            db=settings.redis_database("corpus_config")
        )

    def save(self, config: Corpus) -> None:
        self.client.set(
            f"{config.tenant_id}:{config.name}",
            json.dumps(_to_dict(config), ensure_ascii=False)
        )

        self.client.bgsave()

    def config_of_tenant_and_name(self, tenant_id: str, name: str) -> Optional[Corpus]:
        value = self.client.get(f"{tenant_id}:{name}")

        if not value:
            return None

        raw_config = json.loads(value)

        config = Corpus(
            raw_config.get("tenant_id"),
            raw_config.get("corpus_name"),
            raw_config.get("sitemaps")
        )

        if raw_config.get("description"):
            config.description = raw_config.get("description")

        if raw_config.get("request_headers"):
            config.request_headers = raw_config.get("request_headers")

        if raw_config.get("selector_mapping"):
            config.selector_mapping = raw_config.get("selector_mapping")

        if raw_config.get("excluded_tags"):
            config.excluded_tags = raw_config.get("excluded_tags")

        if raw_config.get("excluded_selectors"):
            config.excluded_selectors = raw_config.get("excluded_selectors")

        if raw_config.get("url_address_pattern"):
            config.url_address_pattern = raw_config.get("url_address_pattern")

        if raw_config.get("custom_request_fields"):
            config.custom_request_fields = raw_config.get("custom_request_fields")

        return config

    def configs_of_tenant(self, tenant_id: str) -> List[Corpus]:
        pass

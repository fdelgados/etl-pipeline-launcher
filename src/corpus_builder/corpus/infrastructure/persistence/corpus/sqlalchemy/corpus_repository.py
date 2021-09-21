from typing import Optional, List

from shared_context.infrastructure.persistence.sqlalchemy import Repository

from shared import settings

from corpus_builder.corpus.domain.model.corpus import Corpus, CorpusRepository


class CorpusRepositoryImpl(CorpusRepository, Repository):
    def __init__(self):
        super().__init__(Corpus, settings.database_dsn("corpus_builder"))

    def config_of_tenant_and_name(self, tenant_id: str, name: str) -> Optional[Corpus]:
        return self.find(_name=name, _tenant_id=tenant_id)

    def configs_of_tenant(self, tenant_id: str) -> List[Corpus]:
        return self.find_all(_tenant_id=tenant_id)

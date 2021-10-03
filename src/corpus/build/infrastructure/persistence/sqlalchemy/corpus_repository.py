from typing import Optional, List

from shared.infrastructure.persistence.sqlalchemy.repository import Repository

import shared.infrastructure.environment.globalvars as glob

from corpus.build.domain.model.corpus import Corpus, CorpusRepository


class CorpusRepositoryImpl(CorpusRepository, Repository):
    def __init__(self):
        super().__init__(Corpus, glob.settings.database_dsn("corpus"))

    def corpus_of_tenant_and_name(self, tenant_id: str, name: str) -> Optional[Corpus]:
        return self.find(_name=name, _tenant_id=tenant_id)

    def corpora_of_tenant(self, tenant_id: str) -> List[Corpus]:
        return self.find_all(_tenant_id=tenant_id)

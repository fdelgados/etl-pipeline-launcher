from duplicates.similarity.domain.model.duplicate import DuplicateRepository, Duplicate
from shared.infrastructure.persistence.sqlalchemy.repository import Repository


class DuplicateRepositoryImpl(DuplicateRepository, Repository):
    def __init__(self, dsn: str):
        super().__init__(Duplicate, dsn)

import shared.infrastructure.environment.globalvars as glob

from duplicates.similarity.domain.model.duplicate import DuplicateRepository, Duplicate
from shared.infrastructure.persistence.sqlalchemy.repository import Repository


class DuplicateRepositoryImpl(DuplicateRepository, Repository):
    def __init__(self):
        super().__init__(Duplicate, glob.settings.database_dsn("duplicates"))

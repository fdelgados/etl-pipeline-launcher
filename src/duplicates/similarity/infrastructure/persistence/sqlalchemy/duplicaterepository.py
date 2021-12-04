import shared.infrastructure.environment.globalvars as global_vars

from duplicates.similarity.domain.model.duplicate import (
    DuplicateRepository,
    Duplicate,
)
from shared.infrastructure.persistence.sqlalchemy.repository import Repository


class DuplicateRepositoryImpl(DuplicateRepository, Repository):
    def __init__(self):
        super().__init__(
            Duplicate,
            global_vars.settings.database_dsn("duplicates")
        )

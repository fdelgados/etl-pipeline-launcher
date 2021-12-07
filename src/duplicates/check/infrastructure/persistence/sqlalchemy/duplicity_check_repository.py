import shared.infrastructure.environment.globalvars as global_vars

from shared.infrastructure.persistence.sqlalchemy.repository import Repository

from duplicates.check.domain.model.duplicitycheck import (
    DuplicityCheck,
    DuplicityCheckRepository
)


class DuplicityCheckRepositoryImpl(DuplicityCheckRepository, Repository):
    def __init__(self):
        super().__init__(
            DuplicityCheck, global_vars.settings.database_dsn("duplicates")
        )

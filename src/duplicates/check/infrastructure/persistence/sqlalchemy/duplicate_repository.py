from datetime import datetime

from typing import List

import shared.infrastructure.environment.globalvars as global_vars

from duplicates.check.domain.model.duplicate import (
    DuplicateRepository,
    Duplicate,
)
from duplicates.check.domain.model.duplicitycheck import DuplicityCheckId

from shared.infrastructure.persistence.sqlalchemy.repository import Repository


class DuplicateRepositoryImpl(DuplicateRepository, Repository):
    def __init__(self):
        super().__init__(
            Duplicate, global_vars.settings.database_dsn("duplicates")
        )

    def duplicates_since(self, since: datetime) -> List[Duplicate]:
        session = self._session()
        query = session.query(self._aggregate).filter(
            Duplicate._checked_on >= since
        ).order_by(Duplicate._checked_on.desc())

        results = query.all()

        session.close()
        self._engine.dispose()

        return results

    def duplicates_of_check(self, check_id: DuplicityCheckId) \
            -> List[Duplicate]:

        session = self._session()
        query = session.query(self._aggregate).filter_by(
            _check_id=check_id
        ).order_by(Duplicate._checked_on.desc())

        results = query.all()

        session.close()
        self._engine.dispose()

        return results

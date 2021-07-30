from abc import ABC

from shared_context.domain.model import Repository


class TenantRepository(Repository, ABC):
    pass

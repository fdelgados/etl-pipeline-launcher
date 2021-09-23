from corpus_builder.build.domain.model.build import (
    BuildId,
    BuildStatus,
    BuildRepository,
)
from corpus_builder.build.domain.service.status.requests_counter import RequestsCounter
from corpus_builder.shared.domain.model.tenant_id import TenantId


class BuildStatusChecker:
    def __init__(
        self, build_repository: BuildRepository, requests_counter: RequestsCounter
    ):
        self._build_repository = build_repository
        self._requests_counter = requests_counter

    def retrieve_status(self, tenant_id: TenantId, build_id: BuildId) -> BuildStatus:
        build = self._build_repository.build_of_tenant_and_id(tenant_id.value, build_id)
        count = self._requests_counter.count(build_id)

        return BuildStatus(
            build.id.value,
            build.total_pages,
            count,
            build.started_on,
            build.is_completed,
        )

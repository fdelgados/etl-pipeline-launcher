import abc

from shared.domain.bus.event import DomainEventSubscriber
from corpus.build.domain.event.urls_retrieved import UrlsRetrieved
from corpus.build.domain.event.build_completed import BuildCompleted
from corpus.build.domain.event.build_aborted import BuildAborted
from corpus.build.domain.model.build import BuildRepository, Build, BuildId
from corpus.build.domain.service.build_stats import BuildStats


class UpdateBuildSubscriber(DomainEventSubscriber, metaclass=abc.ABCMeta):
    def __init__(self, build_repository: BuildRepository):
        super().__init__()

        self._build_repository = build_repository

    def _retrieve_build(self, tenant_id: str, build_id: str) -> Build:
        build = self._build_repository.build_of_tenant_and_id(
            tenant_id,
            BuildId(build_id),
        )

        if not build:
            raise ValueError

        return build


class UpdateTotalPagesOnUrlsRetrieved(UpdateBuildSubscriber):
    def handle(self, domain_event: UrlsRetrieved) -> None:
        try:
            build = self._retrieve_build(
                domain_event.tenant_id,
                domain_event.build_id,
            )

            build.total_requests = domain_event.total_pages

            self._build_repository.save(build)
        except ValueError:
            pass


class UpdateBuildStatsOnBuildCompleted(UpdateBuildSubscriber):
    def __init__(
        self,
        build_repository: BuildRepository,
        build_stats_service: BuildStats,
    ):
        super().__init__(build_repository)

        self._build_stats_service = build_stats_service

    def handle(self, domain_event: BuildCompleted) -> None:
        try:
            build = self._retrieve_build(
                domain_event.tenant_id,
                domain_event.build_id,
            )

            self._build_stats_service.update_counts(build)

            self._build_repository.save(build)
        except ValueError:
            pass


class UpdateBuildStatsOnBuildAborted(UpdateBuildSubscriber):
    def __init__(
        self,
        build_repository: BuildRepository,
        build_stats_service: BuildStats,
    ):
        super().__init__(build_repository)

        self._build_stats_service = build_stats_service

    def handle(self, domain_event: BuildAborted) -> None:
        try:
            build = self._retrieve_build(
                domain_event.tenant_id,
                domain_event.build_id,
            )

            self._build_stats_service.update_counts(build)

            self._build_repository.save(build)
        except ValueError:
            pass

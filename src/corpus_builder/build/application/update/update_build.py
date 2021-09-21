from corpus_builder.build.domain.event.urls_retrieved import UrlsRetrieved
from corpus_builder.build.domain.model.build import BuildRepository, BuildId


class UpdateTotalPagesOnUrlsRetrieved:
    def __init__(self, build_repository: BuildRepository):
        self._build_repository = build_repository

    def __call__(self, event: UrlsRetrieved):
        build = self._build_repository.build_of_tenant_and_id(
            event.tenant_id,
            BuildId(event.build_id)
        )

        if not build:
            return

        build.total_pages = event.total_pages

        self._build_repository.save(build)

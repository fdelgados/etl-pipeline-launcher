from corpus_builder.build.domain.service.requests_counter import RequestsCounter
from corpus_builder.build.domain.model.build import Build


class BuildStats:
    def __init__(self, requests_counter: RequestsCounter):
        self._requests_counter = requests_counter

    def update_counts(self, build: Build):
        build.successful_requests = self._requests_counter.count_successful(build.id)
        build.failed_requests = self._requests_counter.count_failed(build.id)

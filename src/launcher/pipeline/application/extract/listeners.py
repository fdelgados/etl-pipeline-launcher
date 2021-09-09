from launcher.pipeline.domain.event.pipeline_launched import PipelineLaunched
from launcher.pipeline.application.extract.data_extractor import ExtractDataCommand, DataExtractor


class PipelineLaunchedListener:
    def __init__(self, extract_data_service: DataExtractor):
        self._extract_data_service = extract_data_service

    def handle(self, event: PipelineLaunched):
        command = ExtractDataCommand(
            event.tenant_id,
            event.pipeline_id,
            event.sitemaps,
            event.url_pattern,
            event.custom_request_header,
            event.selector_mapping,
            event.excluded_tags,
            event.excluded_selectors,
            event.custom_fields
        )

        self._extract_data_service.extract(command)


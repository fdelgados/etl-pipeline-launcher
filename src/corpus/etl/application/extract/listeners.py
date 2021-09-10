from corpus.etl.domain.event.etl_started import EtlStarted
from corpus.etl.application.extract.data_extractor import ExtractDataCommand, DataExtractor


class ExtractDataOnEtlStarted:
    def __init__(self, extract_data_service: DataExtractor):
        self._extract_data_service = extract_data_service

    def handle(self, event: EtlStarted):
        command = ExtractDataCommand(
            event.tenant_id,
            event.etl_id,
            event.sitemaps,
            event.url_pattern,
            event.custom_request_header,
            event.selector_mapping,
            event.excluded_tags,
            event.excluded_selectors,
            event.custom_fields
        )

        self._extract_data_service.extract(command)


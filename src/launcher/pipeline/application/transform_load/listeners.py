from launcher.pipeline.domain.event.extraction_completed import ExtractionCompleted
from launcher.pipeline.application.transform_load.data_transformer import DataTransformerCommand, DataTransformer


class TransformDataOnExtractionCompleted:
    def __init__(self, data_transformer_service: DataTransformer):
        self._data_transformer_service = data_transformer_service

    def handle(self, event: ExtractionCompleted):
        command = DataTransformerCommand(event.pipeline_id)

        self._data_transformer_service.transform(command)

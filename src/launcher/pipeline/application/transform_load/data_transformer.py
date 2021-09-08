from dataclasses import dataclass


@dataclass(frozen=True)
class DataTransformerCommand:
    pipeline_id: str


class DataTransformer:
    def transform(self, command: DataTransformerCommand):
        pass

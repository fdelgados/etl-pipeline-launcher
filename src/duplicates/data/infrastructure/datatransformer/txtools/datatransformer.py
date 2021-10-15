from txtools.normalizer import clean_text

from typing import List

from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datatransformer import DataTransformer
from duplicates.data.domain.model.transformedpagecontent import TransformedPageContent


class DataTransformerImpl(DataTransformer):
    def transform(self, data: List[Page]) -> List[TransformedPageContent]:
        content = []

        for page in data:
            content.append(
                TransformedPageContent(
                    page.url,
                    clean_text(page.content).lower(),
                )
            )

        return content

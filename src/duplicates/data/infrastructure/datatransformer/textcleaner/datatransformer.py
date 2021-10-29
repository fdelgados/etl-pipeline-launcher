from typing import List

from textcleaner import TextCleaner

from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datatransformer import DataTransformer
from duplicates.data.domain.model.transformedpagecontent import TransformedPageContent


class DataTransformerImpl(DataTransformer):
    def transform(self, data: List[Page]) -> List[TransformedPageContent]:
        content = []

        cleaner = TextCleaner()
        for page in data:
            content.append(
                TransformedPageContent(
                    page.url,
                    cleaner.clean(page.content),
                )
            )

        return content

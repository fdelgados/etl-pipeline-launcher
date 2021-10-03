from txtools.normalizer import clean_text

from typing import List

from duplicates.data.domain.model.page import Page
from duplicates.data.domain.service.datatransformer import DataTransformer
from duplicates.data.domain.model.cleanpage import CleanPageContent


class DataTransformerImpl(DataTransformer):
    def transform(self, data: List[Page]) -> List[CleanPageContent]:
        content = []

        for page in data:
            content.append(
                CleanPageContent(
                    page.url.address,
                    clean_text(page.content).lower(),
                )
            )

        return content

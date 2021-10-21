import os
import pandas as pd

from typing import List

import shared.infrastructure.environment.globalvars as glob

from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContentRepository,
    TransformedPageContent,
)


class TransformedPageContentRepositoryImpl(TransformedPageContentRepository):
    def __init__(self):
        self._data_frame = None

    def save_all(
        self, report_name: str, transformed_page_content: List[TransformedPageContent]
    ):
        content = []

        for clean_page in transformed_page_content:
            content.append(
                {"url": clean_page.url.address, "content": clean_page.content}
            )

        content_df = pd.DataFrame(content, columns=["url", "content"], dtype="object")

        content_file = glob.settings.duplicates_content_file(report_name)

        _create_content_dir(content_file)

        content_df.to_csv(content_file, index=False)

    def size_of_report(self, report_name: str) -> int:
        content_file = glob.settings.duplicates_content_file(report_name)
        content_df = pd.read_csv(content_file)

        return len(content_df.index)


def _create_content_dir(content_file: str):
    content_dir, _ = content_file.rsplit("/", 1)

    os.makedirs(content_dir, exist_ok=True)

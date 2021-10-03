import os
import pandas as pd

from typing import List

import shared.infrastructure.environment.globalvars as glob

from duplicates.data.domain.model.cleanpage import CleanPageContent
from duplicates.data.domain.service.dataloader import DataLoader
from duplicates.report.domain.model.report import Report


class DataLoaderImpl(DataLoader):
    def load(self, data: List[CleanPageContent], report: Report) -> None:
        content = []

        for clean_page in data:
            content.append(
                {"url": clean_page.url, "content": clean_page.content}
            )

        content_df = pd.DataFrame(content, columns=["url", "content"], dtype="object")

        content_file = glob.settings.duplicates_content_file(
            report.name.replace(" ", "_").lower()
        )

        _create_content_dir(content_file)

        content_df.to_csv(content_file, index=False)


def _create_content_dir(content_file: str):
    content_dir, _ = content_file.rsplit("/", 1)

    os.makedirs(content_dir, exist_ok=True)

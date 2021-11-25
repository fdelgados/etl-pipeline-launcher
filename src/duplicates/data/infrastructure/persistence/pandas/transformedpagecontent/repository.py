import os
from typing import List, Optional

import pandas as pd

import shared.infrastructure.environment.globalvars as glob
from shared.domain.model.valueobject.url import Url

from duplicates.data.domain.model.transformedpagecontent import (
    TransformedPageContentRepository,
    TransformedPageContent,
)


class TransformedPageContentRepositoryImpl(TransformedPageContentRepository):
    _URL_COLUMN = "url"
    _CONTENT_COLUMN = "content"

    def __init__(self):
        self._data_frame = None

    def add_all(
        self,
        tenant_id: str,
        transformed_page_content: List[TransformedPageContent],
        as_new: Optional[bool] = True,
    ) -> None:
        records = []
        for clean_page in transformed_page_content:
            records.append(
                {
                    self._URL_COLUMN: clean_page.url.address,
                    self._CONTENT_COLUMN: clean_page.content,
                }
            )

        data_frame = pd.DataFrame(data=records)

        if not as_new:
            try:
                current_data_frame = _get_data_frame(tenant_id)
                data_frame = data_frame.append(
                    current_data_frame, ignore_index=True
                )
            except FileNotFoundError:
                pass

        data_frame.drop_duplicates(
            subset=[self._URL_COLUMN],
            keep="last",
            inplace=True,
            ignore_index=True,
        )

        content_file = glob.settings.duplicates_content_file(tenant_id)

        _create_content_dir(content_file)

        data_frame.to_csv(content_file, index=False)

    def get_all(self, tenant_id: str) -> List[TransformedPageContent]:
        content = []
        try:
            data_frame = _get_data_frame(tenant_id)

            for _, row in data_frame.iterrows():
                content.append(
                    TransformedPageContent(
                        Url(row[self._URL_COLUMN]),
                        row[self._CONTENT_COLUMN],
                    )
                )

            return content
        except FileNotFoundError:
            return content

    def size(self, tenant_id: str) -> int:
        try:
            data_frame = _get_data_frame(tenant_id)

            return len(data_frame.index)
        except FileNotFoundError:
            return 0


def _create_content_dir(content_file: str):
    content_dir, _ = content_file.rsplit("/", 1)

    os.makedirs(content_dir, exist_ok=True)


def _get_data_frame(tenant_id: str) -> Optional[pd.DataFrame]:
    content_file = glob.settings.duplicates_content_file(tenant_id)

    if not os.path.isfile(content_file):
        raise FileNotFoundError("Content file for tenant does not exists")

    return pd.read_csv(content_file)

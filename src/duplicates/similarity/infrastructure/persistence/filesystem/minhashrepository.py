import os
import pickle

from typing import Dict

import shared.infrastructure.environment.globalvars as glob

from duplicates.similarity.domain.model.minhash import (
    MinHash,
    MinHashRepository,
)


class MinHashRepositoryImpl(MinHashRepository):
    def add_all_of_tenant(self, tenant_id: str, minhashes: Dict[str, MinHash]):
        filename = glob.settings.duplicates_minhashes_file(tenant_id)
        _create_minhashes_dir(filename)

        with open(filename, "wb") as file:
            pickle.dump(minhashes, file)

    def get_all_of_tenant(self, tenant_id: str) -> Dict[str, MinHash]:
        filename = glob.settings.duplicates_minhashes_file(tenant_id)

        with open(filename, "rb") as file:
            return pickle.load(file)


def _create_minhashes_dir(content_file: str):
    content_dir, _ = content_file.rsplit("/", 1)

    os.makedirs(content_dir, exist_ok=True)

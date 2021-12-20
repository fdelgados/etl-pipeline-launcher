from typing import Dict

import pandas as pd

import shared.infrastructure.environment.globalvars as glob

from duplicates.data.domain.service.datagatherer import DataGatherer
from duplicates.data.domain.model.page import Page, NullPage
from duplicates.report.domain.model.report import (
    Report,
    ReportId,
    DuplicateRepository,
    Duplicate,
)


def _find_in_dir(
    pages: Dict[str, Page], duplicates: Dict[str, Duplicate], address: str
) -> dict:
    duplicate = duplicates.get(address)

    if not duplicate:
        return {
            "duplicate_page": NullPage(),
            "similarity": None,
        }

    return {
        "duplicate_page": pages.get(duplicate.duplicate_url.address),
        "similarity": duplicate.similarity,
    }


def _build_record(page, duplicate_page, similarity):
    course_info = page.datalayer.get("course")
    methodologies = glob.settings.site_data("methodologies")

    course_data = {
        "search_id": course_info.get("searchId"),
        "course_id": course_info.get("id"),
        "center_id": course_info.get("center").get("id"),
        "center_name": course_info.get("center").get("name"),
        "h1": course_info.get("name"),
        "methodology": methodologies[course_info.get("methodology").get("id")],
        "country": course_info.get("globalSearchId")[0:2],
        "url": page.url.address,
    }

    duplicate_course_info = duplicate_page.datalayer.get("course")

    duplicate_course_data = {
        "matching_search_id": duplicate_course_info.get("searchId")
        if not duplicate_page.is_null()
        else None,
        "matching_course_id": duplicate_course_info.get("id")
        if not duplicate_page.is_null()
        else None,
        "matching_center_id": duplicate_course_info.get("center").get("id")
        if not duplicate_page.is_null()
        else None,
        "matching_center_name": duplicate_course_info.get("center").get("name")
        if not duplicate_page.is_null()
        else None,
        "matching_h1": duplicate_course_info.get("name")
        if not duplicate_page.is_null()
        else None,
        "matching_methodology": methodologies[
            duplicate_course_info.get("methodology").get("id")
        ]
        if not duplicate_page.is_null()
        else None,
        "matching_country": duplicate_course_info.get("globalSearchId")[0:2]
        if not duplicate_page.is_null()
        else None,
        "matching_url": duplicate_page.url.address,
        "similarity": similarity,
    }

    return {**course_data, **duplicate_course_data}


class ResultsRetriever:
    def __init__(
        self,
        data_gatherer: DataGatherer,
        duplicate_repository: DuplicateRepository,
    ):
        self._data_gatherer = data_gatherer
        self._duplicate_repository = duplicate_repository

    def retrieve(self, report: Report):
        pages = self._retrieve_pages(report)
        duplicates = self._retrieve_duplicates(report.report_id)

        records = []

        for address, page in pages.items():
            if not page.datalayer:
                continue

            duplicate = _find_in_dir(pages, duplicates, address)

            duplicate_page = duplicate.get("duplicate_page")

            records.append(
                _build_record(
                    page,
                    duplicate_page,
                    duplicate.get("similarity"),
                )
            )

        data_frame = pd.DataFrame(data=records)
        data_frame.sort_values(
            by=["similarity"], ascending=False, inplace=True
        )
        file_name = glob.settings.report_results_file(
            report.tenant_id,
            report.name.replace(" ", "_").lower(),
        )
        data_frame.to_csv(file_name, index=False)

    def _retrieve_pages(self, report: Report) -> Dict[str, Page]:
        pages = self._data_gatherer.gather(
            report.from_corpus, report.corpus_build_id
        )

        addresses = [page.url.address for page in pages]

        return dict(zip(addresses, pages))

    def _retrieve_duplicates(
        self, report_id: ReportId
    ) -> Dict[str, Duplicate]:
        page_size = 500
        offset = 0
        d = []

        while True:
            duplicates = self._duplicate_repository.search_all_by_report_id(
                report_id,
                page_size,
                offset,
            )

            if not duplicates:
                break

            d.extend(duplicates)
            offset += page_size

        addresses = [duplicate.url.address for duplicate in d]

        return dict(zip(addresses, d))
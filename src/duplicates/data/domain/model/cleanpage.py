from dataclasses import dataclass


@dataclass(frozen=True)
class CleanPageContent:
    url: str
    content: str

import multiprocessing
from typing import List
from shared_context.domain.events import DomainEvent
from shared import Application


class DomainEventDispatcher:
    @classmethod
    def dispatch(cls, domain_events: List[DomainEvent]) -> None:
        for domain_event in domain_events:
            cls._do_dispatch(domain_event)

    @staticmethod
    def _do_dispatch(domain_event: DomainEvent) -> None:
        domain_event_name = _classname(domain_event)
        event_handlers = Application.container().event_handlers(domain_event_name)

        jobs = []
        for subscriber in event_handlers:
            process = multiprocessing.Process(target=subscriber, args=(domain_event,))
            jobs.append(process)

        for job in jobs:
            job.start()


def _classname(obj):
    cls = type(obj)
    module = cls.__module__
    name = cls.__qualname__
    if module is not None and module != "__builtin__":
        name = f"{module}.{name}"

    return name

import multiprocessing

from shared import Application, Utils
from shared.domain.bus.event import EventBus, DomainEvent
from shared.domain.event.event_store import store_event


class InMemoryEventBus(EventBus):
    @store_event
    def _do_publish(self, domain_event: DomainEvent) -> None:
        domain_event_name = Utils.class_fullname(domain_event)
        event_handlers = Application.container().event_handlers(domain_event_name)

        jobs = []
        for subscriber in event_handlers:
            if (
                subscriber.subscribed_to()
                and not domain_event.event_name() in subscriber.subscribed_to()
            ):
                continue

            process = multiprocessing.Process(
                target=subscriber.handle, args=(domain_event,)
            )
            jobs.append(process)

        for job in jobs:
            job.start()

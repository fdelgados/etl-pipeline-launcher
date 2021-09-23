import unittest

from faker import Faker
from shared.domain.event.event import DomainEvent


class DomainEventTest(unittest.TestCase):
    def setUp(self) -> None:
        self._create_domain_event()

    def test_if_returns_proper_event_name_when_is_instantiated(self) -> None:
        self.assertEqual(self._domain_event.type_name(), "FakeDomainEvent")

    def test_if_returns_proper_type_name_when_is_not_instantiated(self) -> None:
        class FakeDomainEvent(DomainEvent):
            pass

        self.assertEqual(FakeDomainEvent.type_name(), "FakeDomainEvent")

    def _create_domain_event(self) -> None:
        class FakeDomainEvent(DomainEvent):
            pass

        fake = Faker()
        self._domain_event = FakeDomainEvent(fake.uuid4())

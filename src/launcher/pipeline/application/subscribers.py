from launcher.pipeline.domain.event import PipelineLaunched
from shared.domain.service.messaging.publisher import EventPublisher


class NotifyPipelineLaunchRequest:
    def __init__(self, event_publisher: EventPublisher):
        self._event_publisher = event_publisher

    def handle(self, event: PipelineLaunched):
        self._event_publisher.publish(event, 'etl_pipeline.launcher.pipelines')

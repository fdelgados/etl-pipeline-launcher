from launcher.pipeline.domain.event import PipelineLaunched
from shared.domain.service.messaging.publisher import Publisher


class NotifyPipelineLaunchRequest:
    def __init__(self, message_publisher: Publisher):
        self._message_publisher = message_publisher

    def handle(self, event: PipelineLaunched):
        self._message_publisher.publish(str(event), 'pipeline_launches')

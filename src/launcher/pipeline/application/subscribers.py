from launcher.pipeline.domain.event import PipelineLaunched


class NotifyPipelineLaunchRequest:
    def handle(self, event: PipelineLaunched):
        f = open("/demofile3.txt", "w")
        f.write("{} {} {}".format(event.tenant_id, event.pipeline_id, event.occurred_on))
        f.close()

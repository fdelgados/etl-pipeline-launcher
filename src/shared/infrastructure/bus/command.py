from shared import Utils, Application
from shared.domain.bus.command import (
    Command,
    CommandHandler,
    CommandBus,
    CommandNotRegisteredError,
    CommandNotCallableError,
)


class CommandBusImpl(CommandBus):
    def dispatch(self, command: Command) -> None:
        container = Application.container()

        command_fullname = Utils.class_fullname(command)
        module, command_name = command_fullname.rsplit(".", maxsplit=1)

        handler_id = "{}.{}_handler".format(
            module, Utils.camel_case_to_snake(command_name)
        )

        command_handler: CommandHandler = container.get(handler_id)

        if not command_handler:
            raise CommandNotRegisteredError(command)

        if not isinstance(command_handler, CommandHandler):
            raise CommandNotRegisteredError(command)

        if not hasattr(command_handler, "handle") or not callable(
            command_handler.handle
        ):
            raise CommandNotCallableError(command)

        command_handler.handle(command)

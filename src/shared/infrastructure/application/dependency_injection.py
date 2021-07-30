import os
from importlib import util
import xml.etree.ElementTree as ElementTree
from dependency_injector import containers

from shared.infrastructure.application.settings import Settings


def _create_container():
    service_container = containers.DynamicContainer()
    services = _get_services()
    service_provider_cls = _import_cls('dependency_injector.providers.Factory')

    for id, info in services.items():
        _create_service(services, service_container, service_provider_cls, id, info)

    class Container:
        @classmethod
        def get(cls, service_id: str):
            return getattr(service_container, service_id.replace('.', '_'))()

    return Container


def _get_services():
    services_file = Settings.services_file()
    services = {}

    tree = ElementTree.parse(services_file)
    root = tree.getroot()

    for service in root:
        if service.tag != 'service':
            continue

        service_data = {'class_name': service.attrib['class'], 'arguments': []}

        for service_argument in service:
            if service_argument.tag != 'argument':
                continue

            service_data['arguments'].append(
                {
                    'type': service_argument.attrib['type'],
                    'name': service_argument.attrib['name'],
                    'value': service_argument.attrib['value']
                }
            )

        services[service.attrib['id']] = service_data

    return services


def _import_cls(full_class_name: str):
    path_components = full_class_name.split('.')
    class_name = path_components[-1]
    mod = '.'.join(path_components[:-1])

    spec = util.find_spec(mod)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, class_name)


def _create_service(services, service_container, service_provider_cls, id: str, info):
    service_key = id.replace('.', '_')
    if hasattr(service_container, service_key):
        return getattr(service_container, service_key)

    service_args = info.get('arguments')
    args = {}

    for argument in service_args:
        if argument.get('type') == 'config':
            args[argument['name']] = os.environ.get(argument['value'])
        elif argument.get('type') == 'parameter':
            args[argument['name']] = argument['value']
        elif argument.get('type') == 'service':
            args[argument['name']] = _create_service(
                services, service_container,
                service_provider_cls,
                argument['value'],
                services[argument['value']]
            )

    service_cls = _import_cls(info.get('class_name'))
    setattr(service_container, service_key, service_provider_cls(service_cls, **args))

    return getattr(service_container, service_key)


def _get_event_handlers():
    event_handlers_file = Settings.event_handlers_file()
    events = {}

    tree = ElementTree.parse(event_handlers_file)
    root = tree.getroot()

    for event in root:
        if event.tag != 'event':
            continue

        event_class_name = event.attrib['class']
        events[event_class_name] = {'class': _import_cls(event_class_name), 'subscribers': []}

        for event_handler in event:
            if event_handler.tag != 'handler':
                continue

            events[event_class_name]['subscribers'].append(_import_cls(event_handler.attrib['class']))

    return events


container = _create_container()
event_handlers = _get_event_handlers()

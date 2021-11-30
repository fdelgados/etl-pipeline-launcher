from __future__ import annotations

import re
import glob

from importlib import util

from shared.infrastructure.environment.settings import Settings
from shared.infrastructure.logging.file.logger import FileLogger


class Bootstrap:
    def __init__(self):
        self.settings = Settings.common_settings()

        self.logger = FileLogger("boot")

        self.generate_db_maps()

    def generate_db_maps(self) -> Bootstrap:
        self.logger.info("Generating database tables mappings")
        for mapping_class in self._db_mapping_classes():
            module_name, class_name = mapping_class.rsplit(".", 1)
            context, _ = module_name.split(".", 1)

            try:
                spec = util.find_spec(module_name)
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)

                class_ = getattr(module, class_name)
                mapper = class_()
                mapper.map_entities()

                self.logger.info("Database tables mappings generated")
            except (ModuleNotFoundError, AttributeError):
                continue

        return self

    def _db_mapping_classes(self):
        contexts_dir = self.settings.get("application").get("contexts_dir")

        context_mapping_files = {}
        mapping_modules = []
        for context in Settings.contexts():
            mapping_file = (
                "{}/{}/shared/infrastructure/persistence"
                "/sqlalchemy/mapping.py"
            )

            mapping_files = glob.glob(
                mapping_file.format(contexts_dir, context)
            )

            context_mapping_files[context] = mapping_files

        for context, files in context_mapping_files.items():
            mapping_class_prefix = (
                context.replace("_", " ").title().replace(" ", "")
            )
            for file in files:
                module_name = file.replace(f"{contexts_dir}/", "").replace(
                    "/", "."
                )
                module_name = re.sub(r"\.py$", "", module_name)
                module_name = "{}.{}Mapping".format(
                    module_name, mapping_class_prefix
                )
                mapping_modules.append(module_name)

        return mapping_modules

    def api_title(self) -> str:
        return self.settings.get("api").get("title")

    def api_doc_path(self) -> str:
        return self.settings.get("api").get("doc_path", "/doc")

    def api_version(self) -> int:
        return self.settings.get("api").get("version")

    def api_version_str(self) -> str:
        return (
            self.settings.get("api")
            .get("version_str")
            .format(self.api_version())
        )

    def api_prefix(self, path: str) -> str:
        api_prefix = (
            self.settings.get("api").get("prefix").format(self.api_version())
        )

        return f"{api_prefix}/{path}"

    def flask_config(self) -> dict:
        if not self.settings.get("flask"):
            return {}

        return {
            key.upper(): value
            for (key, value) in self.settings.get("flask").items()
        }

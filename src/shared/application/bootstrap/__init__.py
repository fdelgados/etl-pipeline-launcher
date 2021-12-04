from __future__ import annotations

import os
import re
import glob
import time

from importlib import util

from shared.infrastructure.environment.settings import Settings
from shared.infrastructure.logging.file.logger import FileLogger
import shared.infrastructure.environment.globalvars as global_vars
import shared.infrastructure.dic.container as container


class Bootstrap:
    def __init__(self):
        global_vars.settings = Settings()
        global_vars.container = container.create_container(
            global_vars.settings
        )

        self.settings = Settings.common_settings()

        os.environ["TZ"] = global_vars.settings.time_zone()
        time.tzset()

        self.logger = FileLogger("boot")

        self._generate_db_maps()

    def _generate_db_maps(self) -> Bootstrap:
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
        contexts_dir = global_vars.settings.contexts_dir()

        context_mapping_files = {}
        mapping_modules = []
        for context in global_vars.settings.contexts():
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

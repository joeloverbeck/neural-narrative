from src.base.constants import HERMES_405B, HERMES_405B_FREE, HERMES_70B, CONFIG_FILE
from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager


class ConfigManager:

    def __init__(self, filesystem_manager: FilesystemManager = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def get_heavy_llm(self) -> RequiredString:
        # Loads from the config file what heavy LLM should be used.
        config_data = self._filesystem_manager.load_existing_or_new_json_file(
            RequiredString(CONFIG_FILE)
        )

        if config_data["heavy_llm"].lower() == "hermes_405b":
            return RequiredString(HERMES_405B)
        elif config_data["heavy_llm"].lower() == "hermes_405b_free":
            return RequiredString(HERMES_405B_FREE)
        elif config_data["heavy_llm"].lower() == "hermes_70b":
            return RequiredString(HERMES_70B)
        else:
            raise ValueError(f"Heavy LLM named '{config_data["heavy_llm"]}' unhandled.")

    def get_light_llm(self) -> RequiredString:
        # Loads from the config file what light LLM should be used.
        config_data = self._filesystem_manager.load_existing_or_new_json_file(
            RequiredString(CONFIG_FILE)
        )

        if config_data["light_llm"].lower() == "hermes_70b":
            return RequiredString(HERMES_70B)
        elif config_data["light_llm"].lower() == "hermes_405b":
            return RequiredString(HERMES_405B)
        else:
            raise ValueError(f"Light LLM named '{config_data["light_llm"]}' unhandled.")

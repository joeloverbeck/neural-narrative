from src.constants import HERMES_405B, HERMES_405B_FREE, HERMES_70B
from src.filesystem.filesystem_manager import FilesystemManager


class ConfigManager:

    def __init__(self, filesystem_manager: FilesystemManager = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def get_heavy_llm(self):
        # Loads from the config file what heavy LLM should be used.
        config_data = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_config_file()
        )

        if config_data["heavy_llm"].lower() == "hermes_405b":
            return HERMES_405B
        elif config_data["heavy_llm"].lower() == "hermes_405b_free":
            return HERMES_405B_FREE
        elif config_data["heavy_llm"].lower() == "hermes_70b":
            return HERMES_70B
        else:
            raise ValueError(f"Heavy LLM named '{config_data["heavy_llm"]}' unhandled.")

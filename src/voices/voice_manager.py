from typing import Optional

from src.constants import VOICE_MODELS_FILE
from src.filesystem.filesystem_manager import FilesystemManager


class VoiceManager:
    def __init__(self, filesystem_manager: Optional[FilesystemManager] = None):
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def get_all_tags(self):
        # Get a set of all tags from all voice models
        all_tags = set()
        for tags in self._filesystem_manager.load_existing_or_new_json_file(
            VOICE_MODELS_FILE
        ).values():
            all_tags.update(tags)
        return sorted(all_tags)

    def filter_voice_models_by_tags(self, selected_tags):
        # Filter voice models that have all the selected tags
        filtered_voice_models = {
            vm_name: tags
            for vm_name, tags in self._filesystem_manager.load_existing_or_new_json_file(
                VOICE_MODELS_FILE
            ).items()
            if all(tag in tags for tag in selected_tags)
        }

        return filtered_voice_models

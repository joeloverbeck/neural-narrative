from src.abstracts.command import Command
from src.filesystem.filesystem_manager import FilesystemManager


class CreatePlaythroughCommand(Command):
    def __init__(self, playthrough_name: str, world_template: str):
        assert playthrough_name
        assert world_template

        self._playthrough_name = playthrough_name
        self._world_template = world_template

    def execute(self) -> None:
        filesystem_manager = FilesystemManager()

        # Check if the folder already exists
        if filesystem_manager.does_file_path_exist(
                filesystem_manager.get_file_path_to_playthrough_folder(self._playthrough_name)):
            raise Exception(f"A playthrough with the name '{self._playthrough_name}' already exists.")

        # Checks here if there is such a world template:
        worlds_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file())

        if self._world_template not in worlds_file:
            raise ValueError(f"There is no such world template '{self._world_template}'")

        filesystem_manager.create_folders_along_file_path(
            filesystem_manager.get_file_path_to_playthrough_folder(self._playthrough_name))

        playthrough_metadata = {
            "world_template": self._world_template,
            "time": "0",
            "last_identifiers": {
                "places": "0",
                "characters": "0"
            }
        }

        # Write the initial values to the JSON file
        filesystem_manager.save_json_file(playthrough_metadata,
                                          filesystem_manager.get_file_path_to_playthrough_metadata(
                                              self._playthrough_name))

        # Must also create the map JSON file
        filesystem_manager.save_json_file({}, filesystem_manager.get_file_path_to_map(self._playthrough_name))

        playthrough_path = filesystem_manager.get_file_path_to_playthrough_folder(self._playthrough_name)

        # Confirm that the playthrough has been successfully created
        print(f"Playthrough '{self._playthrough_name}' created successfully at {playthrough_path}.")

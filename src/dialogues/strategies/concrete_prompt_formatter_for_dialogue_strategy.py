from typing import List

from src.dialogues.abstracts.abstract_factories import PlaceDataForDialoguePromptFactory
from src.dialogues.abstracts.strategies import PromptFormatterForDialogueStrategy
from src.filesystem.filesystem_manager import FilesystemManager
from src.time.time_manager import TimeManager


class ConcretePromptFormatterForDialogueStrategy(PromptFormatterForDialogueStrategy):
    def __init__(self, playthrough_name: str, participants: List[dict],
                 character_data: dict,
                 memories: str, prompt_file: str,
                 place_data_for_dialogue_prompt_factory: PlaceDataForDialoguePromptFactory):
        assert playthrough_name
        assert len(participants) >= 2
        assert character_data
        assert prompt_file
        assert place_data_for_dialogue_prompt_factory

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._character_data = character_data
        self._memories = memories
        self._prompt_file = prompt_file
        self._place_data_for_dialogue_prompt_factory = place_data_for_dialogue_prompt_factory

    def do_algorithm(self) -> str:
        filesystem_manager = FilesystemManager()

        # Retrieve the details of the world
        playthrough_metadata_file = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_playthrough_metadata(self._playthrough_name))

        worlds_template = filesystem_manager.load_existing_or_new_json_file(
            filesystem_manager.get_file_path_to_worlds_template_file())

        participant_details = "\n".join(
            [f'{participant["name"]}: {participant["description"]}. Equipment: {participant["equipment"]}' for
             participant in self._participants if
             participant["name"] != self._character_data["name"]])

        time_manager = TimeManager(float(playthrough_metadata_file["time"]["hour"]))

        place_data_for_dialogue_prompt_product = self._place_data_for_dialogue_prompt_factory.create_place_data_for_dialogue_prompt()

        if not place_data_for_dialogue_prompt_product.is_valid():
            raise ValueError(
                f"Wasn't able to produce place data for the dialogue prompt: {place_data_for_dialogue_prompt_product.get_error()}")

        # It could be that there isn't a location involved
        location_name = ""
        location_description = ""

        if place_data_for_dialogue_prompt_product.get()["location_data"]:
            location_name = f"Inside the area {place_data_for_dialogue_prompt_product.get()["area_data"]["name"]}, you are currently in this location: {place_data_for_dialogue_prompt_product.get()["location_data"]["name"]}."
            location_description = f"Here's the description of the location: {place_data_for_dialogue_prompt_product.get()["location_data"]["description"]}"

        return filesystem_manager.read_file(self._prompt_file).format(
            world_name=playthrough_metadata_file["world_template"],
            world_description=worlds_template[playthrough_metadata_file["world_template"]]["description"],
            region_name=place_data_for_dialogue_prompt_product.get()["region_data"]["name"],
            region_description=place_data_for_dialogue_prompt_product.get()["region_data"]["description"],
            area_name=place_data_for_dialogue_prompt_product.get()["area_data"]["name"],
            area_description=place_data_for_dialogue_prompt_product.get()["area_data"]["description"],
            location_name=location_name,
            location_description=location_description,
            hour=time_manager.get_hour(),
            time_group=time_manager.get_time_of_the_day(),
            name=self._character_data["name"],
            participant_details=participant_details,
            description=self._character_data["description"],
            personality=self._character_data["personality"],
            profile=self._character_data["profile"],
            likes=self._character_data["likes"],
            dislikes=self._character_data["dislikes"],
            first_message=self._character_data["first message"],
            speech_patterns=self._character_data["speech patterns"],
            memories=self._memories)

from src.dialogues.abstracts.strategies import PromptFormatterForDialogueStrategy
from src.dialogues.participants import Participants
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.abstracts.abstract_factories import FullPlaceDataFactory
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.time.time_manager import TimeManager


class ConcretePromptFormatterForDialogueStrategy(PromptFormatterForDialogueStrategy):
    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        character_data: dict,
        memories: str,
        prompt_file: str,
        full_place_data_factory: FullPlaceDataFactory,
        filesystem_manager: FilesystemManager = None,
        map_manager: MapManager = None,
        playthrough_manager: PlaythroughManager = None,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._character_data = character_data
        self._memories = memories
        self._prompt_file = prompt_file
        self._full_place_data_factory = full_place_data_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()
        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def do_algorithm(self) -> str:
        full_place_data_product = self._full_place_data_factory.create_full_place_data()

        if not full_place_data_product.is_valid():
            raise ValueError(
                f"Was unable to retrieve the full place data: {full_place_data_product.get_error()}"
            )

        full_place_data = full_place_data_product.get()

        # It could be that there isn't a location involved
        location_name = ""
        location_description = ""

        if full_place_data["location_data"]:
            location_name = f"Inside the area {full_place_data["area_data"]["name"]}, you are currently in this location: {full_place_data["location_data"]["name"]}."
            location_description = f"Here's the description of the location: {full_place_data["location_data"]["description"]}"

        time_manager = TimeManager(self._playthrough_name)

        worlds_template = self._filesystem_manager.load_existing_or_new_json_file(
            self._filesystem_manager.get_file_path_to_worlds_template_file()
        )

        participant_details = "\n".join(
            [
                f'{participant["name"]}: {participant["description"]}. Equipment: {participant["equipment"]}'
                for _, participant in self._participants.get().items()
                if participant["name"] != self._character_data["name"]
            ]
        )

        return self._filesystem_manager.read_file(self._prompt_file).format(
            world_name=self._playthrough_manager.get_world_template(),
            world_description=worlds_template[
                self._playthrough_manager.get_world_template()
            ]["description"],
            region_name=full_place_data["region_data"]["name"],
            region_description=full_place_data["region_data"]["description"],
            area_name=full_place_data["area_data"]["name"],
            area_description=full_place_data["area_data"]["description"],
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
            memories=self._memories,
        )

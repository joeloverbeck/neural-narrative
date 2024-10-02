from src.characters.characters_manager import CharactersManager
from src.constants import (
    TRAVEL_NARRATION_PROMPT_FILE,
    TRAVEL_NARRATION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.playthrough_manager import PlaythroughManager
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.travel_narration_product import TravelNarrationProduct
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class TravelNarrationFactory(BaseToolResponseProvider):
    """
    Factory class to generate travel narration using LLMs.
    """

    def __init__(
            self,
            playthrough_name: str,
            destination_identifier: str,
            produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
            characters_manager: CharactersManager = None,
            playthrough_manager: PlaythroughManager = None,
            filesystem_manager: FilesystemManager = None,
            map_manager: MapManager = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not destination_identifier:
            raise ValueError("destination_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._destination_identifier = destination_identifier

        self._characters_manager = characters_manager or CharactersManager(
            playthrough_name
        )
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            playthrough_name
        )
        self._map_manager = map_manager or MapManager(playthrough_name)

    def generate_travel_narration(self) -> TravelNarrationProduct:
        player_identifier = self._playthrough_manager.get_player_identifier()
        player_data = self._characters_manager.load_character_data(player_identifier)
        player_data["memories"] = self._characters_manager.load_character_memories(
            player_identifier
        )

        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )
        current_place_data = self._map_manager.get_place_full_data(
            current_place_identifier
        )
        destination_place_data = self._map_manager.get_place_full_data(
            self._destination_identifier
        )

        followers_information = self._get_followers_information()

        # Prepare the prompt
        prompt_template = self._read_prompt_file(TRAVEL_NARRATION_PROMPT_FILE)
        formatted_prompt = self._format_prompt(
            prompt_template,
            origin_area_template=self._map_manager.get_current_place_template(),
            origin_area_description=current_place_data["area_data"]["description"],
            destination_area_template=destination_place_data["area_data"]["name"],
            destination_area_description=destination_place_data["area_data"][
                "description"
            ],
            player_name=player_data["name"],
            player_description=player_data["description"],
            player_personality=player_data["personality"],
            player_profile=player_data["profile"],
            player_likes=player_data["likes"],
            player_dislikes=player_data["dislikes"],
            player_speech_patterns=player_data["speech patterns"],
            player_equipment=player_data["equipment"],
            player_memories=player_data["memories"],
            followers_information=followers_information,
        )

        # Generate system content
        tool_data = self._read_tool_file(TRAVEL_NARRATION_TOOL_FILE)
        tool_instructions = self._read_tool_instructions()
        tool_prompt = self._generate_tool_prompt(tool_data, tool_instructions)
        system_content = self._generate_system_content(formatted_prompt, tool_prompt)

        # User content
        user_content = "Write the narration of the travel from the origin area to the destination area, filtered through the first-person perspective of the player, as per the above instructions."

        # Produce tool response
        tool_response = self._produce_tool_response(system_content, user_content)

        # Extract arguments
        arguments = self._extract_arguments(tool_response)

        return TravelNarrationProduct(
            travel_narration=arguments.get("narration", "The travel was uneventful."),
            is_valid=True,
        )

    def _get_followers_information(self) -> str:
        followers_info = ""
        follower_ids = self._playthrough_manager.get_followers()
        followers_data = self._characters_manager.get_full_data_of_characters(
            follower_ids
        )

        for follower in followers_data:
            memories = self._characters_manager.load_character_memories(
                follower["identifier"]
            )
            followers_info += (
                f"Follower name: {follower['name']}\n"
                f"Description: {follower['description']}\n"
                f"Personality: {follower['personality']}\n"
                f"Profile: {follower['profile']}\n"
                f"Likes: {follower['likes']}\n"
                f"Dislikes: {follower['dislikes']}\n"
                f"Speech patterns: {follower['speech patterns']}\n"
                f"Equipment: {follower['equipment']}\n"
                f"Memories:\n{memories}\n\n"
            )
        return followers_info

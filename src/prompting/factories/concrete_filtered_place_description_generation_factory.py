from src.characters.characters_manager import CharactersManager
from src.constants import (
    PLACE_DESCRIPTION_PROMPT_FILE,
    TOOL_INSTRUCTIONS_FILE,
    PLACE_DESCRIPTION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.prompting.abstracts.abstract_factories import (
    FilteredPlaceDescriptionGenerationFactory,
)
from src.prompting.abstracts.factory_products import (
    FilteredPlaceDescriptionGenerationProduct,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_filtered_place_description_generation_product import (
    ConcreteFilteredPlaceDescriptionGenerationProduct,
)
from src.tools import generate_tool_prompt


class ConcreteFilteredPlaceDescriptionGenerationFactory(
    FilteredPlaceDescriptionGenerationFactory
):
    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        place_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        map_manager: MapManager = None,
        characters_manager: CharactersManager = None,
        filesystem_manager: FilesystemManager = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not place_identifier:
            raise ValueError("player_identifier can't be empty.")
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._place_identifier = place_identifier
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def generate_filtered_place_description(
        self,
    ) -> FilteredPlaceDescriptionGenerationProduct:

        # We have the place identifier, so we have to retrieve the data of that place.
        place_type = self._map_manager.determine_place_type(self._place_identifier)

        place_full_data = self._map_manager.get_place_full_data(self._place_identifier)

        place_data = place_full_data[f"{place_type.value}_data"]

        # Now that we have the place data, we need to retrieve the player's data.
        player_data = self._characters_manager.load_character_data(
            self._player_identifier
        )

        # Load player memories
        player_data["memories"] = self._characters_manager.load_character_memories(
            self._player_identifier
        )

        # Now we need to format the prompt to the LLM.
        place_description_prompt = self._filesystem_manager.read_file(
            PLACE_DESCRIPTION_PROMPT_FILE
        ).format(
            place_type=place_type,
            place_template=place_data["name"],
            place_description=place_data["description"],
            player_name=player_data["name"],
            player_description=player_data["description"],
            player_personality=player_data["personality"],
            player_profile=player_data["profile"],
            player_likes=player_data["likes"],
            player_dislikes=player_data["dislikes"],
            player_speech_patterns=player_data["speech patterns"],
            player_equipment=player_data["equipment"],
            player_memories=player_data["memories"],
        )

        system_content = (
            place_description_prompt
            + "\n\n"
            + generate_tool_prompt(
                self._filesystem_manager.read_json_file(PLACE_DESCRIPTION_TOOL_FILE),
                self._filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
            )
        )

        user_content = "Write the description of the indicated place, filtered through the perspective of the character whose data has been provided, as per the above instructions."

        tool_response = self._produce_tool_response_strategy_factory.create_produce_tool_response_strategy().produce_tool_response(
            system_content, user_content
        )

        # Extract the "arguments" dictionary from the tool response
        arguments = tool_response.get("arguments", {})

        description = arguments.get(
            "description", "I'm not sure what to say now about this place."
        )

        return ConcreteFilteredPlaceDescriptionGenerationProduct(
            description, is_valid=True
        )

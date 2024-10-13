from typing import Optional

from src.characters.characters_manager import CharactersManager
from src.characters.factories.character_information_factory import (
    CharacterInformationFactory,
)
from src.constants import (
    PLACE_DESCRIPTION_PROMPT_FILE,
    PLACE_DESCRIPTION_TOOL_FILE,
)
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.map_manager import MapManager
from src.prompting.abstracts.abstract_factories import (
    FilteredPlaceDescriptionGenerationFactory,
)
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.products.concrete_filtered_place_description_generation_product import (
    ConcreteFilteredPlaceDescriptionGenerationProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class ConcreteFilteredPlaceDescriptionGenerationFactory(
    BaseToolResponseProvider, FilteredPlaceDescriptionGenerationFactory
):
    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        place_identifier: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        character_information_factory: CharacterInformationFactory,
        map_manager: MapManager = None,
        characters_manager: CharactersManager = None,
        filesystem_manager: FilesystemManager = None,
        time_manager: TimeManager = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, filesystem_manager)

        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        if not place_identifier:
            raise ValueError("player_identifier can't be empty.")
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._place_identifier = place_identifier
        self._character_information_factory = character_information_factory

        self._map_manager = map_manager or MapManager(self._playthrough_name)
        self._characters_manager = characters_manager or CharactersManager(
            self._playthrough_name
        )
        self._time_manager = time_manager or TimeManager(self._playthrough_name)

    def get_prompt_file(self) -> Optional[str]:
        return PLACE_DESCRIPTION_PROMPT_FILE

    def get_tool_file(self) -> str:
        return PLACE_DESCRIPTION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Write the description of the indicated place, filtered through the perspective of the character whose data has been provided, as per the above instructions."

    def get_prompt_kwargs(self) -> dict:
        # We have the place identifier, so we have to retrieve the data of that place.
        place_type = self._map_manager.determine_place_type(self._place_identifier)

        place_full_data = self._map_manager.get_place_full_data(self._place_identifier)

        place_data = place_full_data[f"{place_type.value}_data"]

        data_for_prompt = {
            "hour": self._time_manager.get_hour(),
            "time_of_the_day": self._time_manager.get_time_of_the_day(),
            "place_type": place_type,
            "place_template": place_data["name"],
            "place_description": place_data["description"],
        }

        data_for_prompt.update(
            {
                "character_information": self._character_information_factory.get_information()
            }
        )

        return data_for_prompt

    def create_product(self, arguments: dict):
        description = arguments.get(
            "description", "I'm not sure what to say now about this place."
        )

        return ConcreteFilteredPlaceDescriptionGenerationProduct(
            description, is_valid=True
        )

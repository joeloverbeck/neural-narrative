from typing import Optional

from src.base.constants import (
    PLACE_DESCRIPTION_PROMPT_FILE,
    PLACE_DESCRIPTION_TOOL_FILE,
)
from src.base.required_string import RequiredString
from src.filesystem.filesystem_manager import FilesystemManager
from src.maps.configs.filtered_place_description_generation_factory_config import (
    FilteredPlaceDescriptionGenerationFactoryConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_factories_config import (
    FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
)
from src.prompting.abstracts.abstract_factories import (
    FilteredPlaceDescriptionGenerationFactory,
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
            config: FilteredPlaceDescriptionGenerationFactoryConfig,
            factories_config: FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
        filesystem_manager: Optional[FilesystemManager] = None,
        time_manager: Optional[TimeManager] = None,
    ):
        super().__init__(
            factories_config.produce_tool_response_strategy_factory, filesystem_manager
        )

        self._config = config
        self._factories_config = factories_config

        self._time_manager = time_manager or TimeManager(self._config.playthrough_name)

    def get_prompt_file(self) -> Optional[str]:
        return PLACE_DESCRIPTION_PROMPT_FILE

    def get_tool_file(self) -> str:
        return PLACE_DESCRIPTION_TOOL_FILE

    def get_user_content(self) -> str:
        return "Write the description of the indicated place, filtered through the perspective of the character whose data has been provided, as per the above instructions."

    def get_prompt_kwargs(self) -> dict:
        # We have the place identifier, so we have to retrieve the data of that place.
        place_type = self._factories_config.place_manager_factory.create_place_manager().determine_place_type(
            self._config.place_identifier
        )

        place_full_data = self._factories_config.map_manager_factory.create_map_manager().get_place_full_data(
            self._config.place_identifier
        )

        place_data = place_full_data[f"{place_type.value}_data"]

        data_for_prompt = {
            "hour": self._time_manager.get_hour(),
            "time_of_the_day": self._time_manager.get_time_of_the_day(),
            "weather": self._factories_config.weathers_manager.get_weather_description(
                self._factories_config.weathers_manager.get_current_weather_identifier()
            ),
            "place_type": place_type.value,
            "place_template": place_data["name"],
            "place_description": place_data["description"],
        }

        data_for_prompt.update(
            {
                "character_information": self._factories_config.character_information_factory.get_information()
            }
        )

        return data_for_prompt

    def create_product(self, arguments: dict):
        description = arguments.get(
            "description", "I'm not sure what to say now about this place."
        )

        return ConcreteFilteredPlaceDescriptionGenerationProduct(
            RequiredString(description), is_valid=True
        )

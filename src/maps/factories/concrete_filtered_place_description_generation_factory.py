from typing import Optional

from pydantic import BaseModel

from src.base.tools import join_with_newline
from src.filesystem.path_manager import PathManager
from src.maps.configs.filtered_place_description_generation_factory_algorithms_config import (
    FilteredPlaceDescriptionGenerationFactoryAlgorithmsConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_config import (
    FilteredPlaceDescriptionGenerationFactoryConfig,
)
from src.maps.configs.filtered_place_description_generation_factory_factories_config import (
    FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
)
from src.prompting.products.concrete_filtered_place_description_generation_product import (
    ConcreteFilteredPlaceDescriptionGenerationProduct,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider
from src.time.time_manager import TimeManager


class ConcreteFilteredPlaceDescriptionGenerationFactory(BaseToolResponseProvider):

    def __init__(
        self,
        config: FilteredPlaceDescriptionGenerationFactoryConfig,
        factories_config: FilteredPlaceDescriptionGenerationFactoryFactoriesConfig,
        algorithms_config: FilteredPlaceDescriptionGenerationFactoryAlgorithmsConfig,
        path_manager: Optional[PathManager] = None,
        time_manager: Optional[TimeManager] = None,
    ):
        super().__init__(
            factories_config.produce_tool_response_strategy_factory,
            path_manager,
        )
        self._config = config
        self._factories_config = factories_config
        self._algorithms_config = algorithms_config
        self._time_manager = time_manager or TimeManager(self._config.playthrough_name)

    def get_prompt_file(self) -> Optional[str]:
        return self._path_manager.get_place_description_prompt_path()

    def get_user_content(self) -> str:
        return "Write the description of the indicated place, filtered through the perspective of the character whose data has been provided, as per the above instructions."

    def get_prompt_kwargs(self) -> dict:
        place_type = self._factories_config.place_manager_factory.create_place_manager().determine_place_type(
            self._config.place_identifier
        )
        place_full_data = (
            self._algorithms_config.get_place_full_data_algorithm.do_algorithm()
        )
        place_data = place_full_data[f"{place_type.value}_data"]

        weather = self._factories_config.weathers_manager.get_weather_description(
            self._algorithms_config.get_current_weather_identifier_algorithm.do_algorithm()
        )
        place_description = place_data["description"]

        data_for_prompt = {
            "hour": self._time_manager.get_hour(),
            "time_of_the_day": self._time_manager.get_time_of_the_day(),
            "weather": weather,
            "place_type": place_type.value,
            "place_template": place_data["name"],
            "place_description": place_description,
        }
        data_for_prompt.update(
            {
                "character_information": self._factories_config.character_information_provider_factory.create_provider(
                    join_with_newline(weather, place_description)
                ).get_information()
            }
        )
        return data_for_prompt

    def create_product_from_base_model(self, response_model: BaseModel):
        return ConcreteFilteredPlaceDescriptionGenerationProduct(
            response_model.description, is_valid=True
        )

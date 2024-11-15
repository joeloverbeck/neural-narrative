import logging
from typing import Optional

from pydantic import BaseModel

from src.base.validators import validate_non_empty_string
from src.characters.products.character_generation_guidelines_product import (
    CharacterGenerationGuidelinesProduct,
)
from src.concepts.algorithms.format_known_facts_algorithm import (
    FormatKnownFactsAlgorithm,
)
from src.filesystem.file_operations import read_file
from src.filesystem.path_manager import PathManager
from src.maps.factories.map_manager_factory import MapManagerFactory
from src.maps.factories.place_manager_factory import PlaceManagerFactory
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider
from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider

logger = logging.getLogger(__name__)


class CharacterGenerationGuidelinesProvider(BaseToolResponseProvider):

    def __init__(
        self,
        playthrough_name: str,
        format_known_facts_algorithm: FormatKnownFactsAlgorithm,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
        places_descriptions_factory: PlacesDescriptionsProvider,
        place_manager_factory: PlaceManagerFactory,
        map_manager_factory: MapManagerFactory,
        path_manager: Optional[PathManager] = None,
    ):
        super().__init__(produce_tool_response_strategy_factory, path_manager)

        validate_non_empty_string(playthrough_name, "playthough_name")

        self._format_known_facts_algorithm = format_known_facts_algorithm
        self._places_descriptions_factory = places_descriptions_factory
        self._place_manager_factory = place_manager_factory
        self._map_manager_factory = map_manager_factory

    def get_prompt_file(self) -> str:
        return self._path_manager.get_character_generation_guidelines_prompt_path()

    def get_prompt_kwargs(self) -> dict:
        places_descriptions = self._places_descriptions_factory.get_information()

        prompt_data = {
            "places_descriptions": places_descriptions,
            "known_facts": self._format_known_facts_algorithm.do_algorithm(
                places_descriptions
            ),
        }
        place_categories = self._place_manager_factory.create_place_manager().get_place_categories(
            self._map_manager_factory.create_map_manager().get_current_place_template(),
            self._place_manager_factory.create_place_manager().get_current_place_type(),
        )
        prompt_data.update(
            {"categories": ", ".join([category for category in place_categories])}
        )

        return prompt_data

    def _read_tool_instructions(self) -> str:
        """Reads the tool instructions from the filesystem."""
        return read_file(self._path_manager.get_tool_instructions_for_instructor_path())

    def get_user_content(self) -> str:
        return "Write three entries that are guidelines for creating interesting characters based on the above combination of places. Follow the provided instructions."

    def create_product_from_base_model(self, response_model: BaseModel):
        return CharacterGenerationGuidelinesProduct(
            response_model.guidelines,
            is_valid=True,
        )

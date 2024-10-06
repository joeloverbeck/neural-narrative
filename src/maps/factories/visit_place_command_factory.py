from src.characters.factories.character_generation_guidelines_factory import (
    CharacterGenerationGuidelinesFactory,
)
from src.movements.commands.visit_place_command import VisitPlaceCommand
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class VisitPlaceCommandFactory:

    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
    ):
        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_visit_place_command(self, place_identifier: str) -> VisitPlaceCommand:
        if not place_identifier:
            raise ValueError("place_identifier can't be empty.")

        return VisitPlaceCommand(
            self._playthrough_name,
            place_identifier,
            CharacterGenerationGuidelinesFactory(
                self._playthrough_name,
                place_identifier,
                self._produce_tool_response_strategy_factory,
            ),
        )

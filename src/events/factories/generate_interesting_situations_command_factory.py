from src.events.commands.generate_interesting_situations_command import (
    GenerateInterestingSituationsCommand,
)
from src.events.factories.interesting_situations_factory import (
    InterestingSituationsFactory,
)
from src.dialogues.transcription import Transcription
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class GenerateInterestingSituationsCommandFactory:
    def __init__(
        self,
        playthrough_name: str,
        produce_tool_response_strategy_factory: ProduceToolResponseStrategyFactory,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._produce_tool_response_strategy_factory = (
            produce_tool_response_strategy_factory
        )

    def create_generate_interesting_situations_command(
        self,
        transcription: Transcription,
    ) -> GenerateInterestingSituationsCommand:
        return GenerateInterestingSituationsCommand(
            playthrough_name=self._playthrough_name,
            interesting_situations_factory=InterestingSituationsFactory(
                transcription, self._produce_tool_response_strategy_factory
            ),
        )

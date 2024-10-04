from src.dialogues.transcription import Transcription
from src.events.commands.generate_interesting_dilemmas_command import (
    GenerateInterestingDilemmasCommand,
)
from src.events.factories.interesting_dilemmas_factory import InterestingDilemmasFactory
from src.prompting.factories.produce_tool_response_strategy_factory import (
    ProduceToolResponseStrategyFactory,
)


class GenerateInterestingDilemmasCommandFactory:
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

    def create_command(
        self,
        transcription: Transcription,
    ) -> GenerateInterestingDilemmasCommand:
        return GenerateInterestingDilemmasCommand(
            playthrough_name=self._playthrough_name,
            interesting_dilemmas_factory=InterestingDilemmasFactory(
                transcription, self._produce_tool_response_strategy_factory
            ),
        )

from typing import List

from src.constants import DIALOGUE_PROMPT_FILE
from src.dialogues.abstracts.strategies import PromptFormatterForDialogueStrategy
from src.dialogues.strategies.concrete_prompt_formatter_for_dialogue_strategy import \
    ConcretePromptFormatterForDialogueStrategy
from src.maps.abstracts.abstract_factories import FullPlaceDataFactory


class PromptFormatterForDialogueStrategyFactory:
    def __init__(self, playthrough_name: str, full_place_data_factory: FullPlaceDataFactory):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._full_place_data_factory = full_place_data_factory

    def create_prompt_formatter_for_dialogue_strategy_factory(self, participants_data: List[dict], character_data: dict,
                                                              memories: str) -> PromptFormatterForDialogueStrategy:
        return ConcretePromptFormatterForDialogueStrategy(
            self._playthrough_name, participants_data,
            character_data,
            memories,
            DIALOGUE_PROMPT_FILE, self._full_place_data_factory)

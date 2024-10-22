from typing import Optional
from src.base.constants import DIALOGUE_PROMPT_FILE
from src.characters.character import Character
from src.characters.factories.character_information_provider import CharacterInformationProvider
from src.dialogues.abstracts.strategies import PromptFormatterForDialogueStrategy
from src.dialogues.participants import Participants
from src.dialogues.strategies.concrete_prompt_formatter_for_dialogue_strategy import \
    ConcretePromptFormatterForDialogueStrategy
from src.maps.providers.places_descriptions_provider import PlacesDescriptionsProvider


class PromptFormatterForDialogueStrategyFactory:

    def __init__(self, playthrough_name: str, purpose: Optional[str],
                 places_descriptions_factory: PlacesDescriptionsProvider):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        self._playthrough_name = playthrough_name
        self._purpose = purpose
        self._places_descriptions_factory = places_descriptions_factory

    def create_prompt_formatter_for_dialogue_strategy_factory(self,
                                                              participants: Participants, character: Character
                                                              ) -> PromptFormatterForDialogueStrategy:
        return ConcretePromptFormatterForDialogueStrategy(self.
                                                          _playthrough_name, participants, self._purpose,
                                                          character.name,
                                                          CharacterInformationProvider(self._playthrough_name,
                                                                                       character.
                                                                                       identifier),
                                                          DIALOGUE_PROMPT_FILE, self.
                                                          _places_descriptions_factory)

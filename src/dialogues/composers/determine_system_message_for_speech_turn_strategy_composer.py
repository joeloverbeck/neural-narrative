from typing import Optional

from src.base.playthrough_manager import PlaythroughManager
from src.dialogues.abstracts.strategies import (
    DetermineSystemMessageForSpeechTurnStrategy,
)
from src.dialogues.factories.determine_system_message_for_speech_turn_strategy_factory import (
    DetermineSystemMessageForSpeechTurnStrategyFactory,
)
from src.dialogues.factories.dialogue_initial_prompting_messages_provider_factory import (
    DialogueInitialPromptingMessagesProviderFactory,
)
from src.dialogues.factories.prompt_formatter_for_dialogue_strategy_factory import (
    PromptFormatterForDialogueStrategyFactory,
)
from src.dialogues.factories.speech_turn_dialogue_system_content_for_prompt_provider_factory import (
    SpeechTurnDialogueSystemContentForPromptProviderFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.maps.composers.places_descriptions_provider_composer import (
    PlacesDescriptionsProviderComposer,
)


class DetermineSystemMessageForSpeechTurnStrategyComposer:

    def __init__(
        self,
        playthrough_name: str,
        participants: Participants,
        purpose: Optional[str],
        messages_to_llm: MessagesToLlm,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")
        self._playthrough_name = playthrough_name
        self._participants = participants
        self._purpose = purpose
        self._messages_to_llm = messages_to_llm
        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._playthrough_name
        )

    def compose(self) -> DetermineSystemMessageForSpeechTurnStrategy:
        prompt_formatter_for_dialogue_strategy_factory = (
            PromptFormatterForDialogueStrategyFactory(
                self._playthrough_name,
                self._purpose,
                PlacesDescriptionsProviderComposer(
                    self._playthrough_name
                ).compose_provider(),
            )
        )
        speech_turn_dialogue_system_content_for_prompt_provider_factory = (
            SpeechTurnDialogueSystemContentForPromptProviderFactory(
                prompt_formatter_for_dialogue_strategy_factory
            )
        )
        dialogue_initial_prompting_messages_provider_factory = (
            DialogueInitialPromptingMessagesProviderFactory(
                self._playthrough_name,
                self._participants,
                speech_turn_dialogue_system_content_for_prompt_provider_factory,
            )
        )
        return DetermineSystemMessageForSpeechTurnStrategyFactory(
            dialogue_initial_prompting_messages_provider_factory
        ).create_determine_system_message_for_speech_turn_strategy(
            self._messages_to_llm
        )

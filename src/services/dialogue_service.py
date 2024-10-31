import logging
from typing import List, Dict, Optional

from flask import session, url_for

from src.base.playthrough_manager import PlaythroughManager
from src.characters.composers.local_information_factory_composer import (
    LocalInformationFactoryComposer,
)
from src.characters.composers.relevant_characters_information_factory_composer import (
    RelevantCharactersInformationFactoryComposer,
)
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.commands.setup_dialogue_command import SetupDialogueCommand
from src.dialogues.composers.load_ongoing_conversation_data_command_factory_composer import (
    LoadOngoingConversationDataCommandFactoryComposer,
)
from src.dialogues.composers.produce_narration_for_dialogue_command_composer import (
    ProduceNarrationForDialogueCommandComposer,
)
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.ambient_narration_provider_factory import (
    AmbientNarrationProviderFactory,
)
from src.dialogues.factories.grow_event_provider_factory import GrowEventProviderFactory
from src.dialogues.factories.narrative_beat_provider_factory import (
    NarrativeBeatProviderFactory,
)
from src.dialogues.factories.web_player_input_factory import WebPlayerInputFactory
from src.dialogues.observers.web_dialogue_observer import WebDialogueObserver
from src.dialogues.observers.web_narration_observer import (
    WebNarrationObserver,
)
from src.dialogues.participants import Participants
from src.dialogues.strategies.ambient_narration_for_dialogue_strategy import (
    AmbientNarrationForDialogueStrategy,
)
from src.dialogues.strategies.event_narration_for_dialogue_strategy import (
    EventNarrationForDialogueStrategy,
)
from src.dialogues.strategies.grow_event_narration_for_dialogue_strategy import (
    GrowEventNarrationForDialogueStrategy,
)
from src.dialogues.strategies.narrative_beat_for_dialogue_strategy import (
    NarrativeBeatForDialogueStrategy,
)
from src.dialogues.strategies.participants_identifiers_strategy import (
    ParticipantsIdentifiersStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_introduce_player_input_into_dialogue_strategy import (
    WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)
from src.dialogues.strategies.web_message_data_producer_for_speech_turn_strategy import (
    WebMessageDataProducerForSpeechTurnStrategy,
)
from src.filesystem.config_loader import ConfigLoader
from src.prompting.composers.produce_tool_response_strategy_factory_composer import (
    ProduceToolResponseStrategyFactoryComposer,
)
from src.prompting.llms import Llms

logger = logging.getLogger(__name__)


class DialogueService:

    def __init__(self):
        self._playthrough_name = session.get("playthrough_name")

    def _process_narration(
        self,
        other_characters_identifiers: List[str],
        purpose: Optional[str],
        narration_type: str,
        narration_strategy: NarrationForDialogueStrategy,
        observer: WebNarrationObserver,
    ) -> dict:
        ProduceNarrationForDialogueCommandComposer(
            self._playthrough_name,
            other_characters_identifiers,
            purpose,
            narration_type,
            observer,
            narration_strategy,
        ).compose_command().execute()

        return observer.get_messages()[0]

    def process_ambient_message(
        self, other_characters_identifiers: List[str], purpose: Optional[str]
    ) -> dict:
        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_ambient_narration(),
            ).compose_factory()
        )

        local_information_factory = LocalInformationFactoryComposer(
            self._playthrough_name
        ).compose_factory()

        ambient_narration_provider_factory = AmbientNarrationProviderFactory(
            self._playthrough_name,
            produce_tool_response_strategy_factory,
            local_information_factory,
        )

        narration_for_dialogue_strategy = AmbientNarrationForDialogueStrategy(
            DialogueManager(self._playthrough_name).load_transcription(),
            ambient_narration_provider_factory,
        )

        web_ambient_narration_observer = WebNarrationObserver()

        return self._process_narration(
            other_characters_identifiers,
            purpose,
            "ambient",
            narration_for_dialogue_strategy,
            web_ambient_narration_observer,
        )

    def process_narrative_beat(
        self, other_characters_identifiers: List[str], purpose: Optional[str]
    ) -> dict:
        if not isinstance(other_characters_identifiers, list):
            raise TypeError(
                f"Expected participants_identifiers to be a list, but was '{type(other_characters_identifiers)}'."
            )

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_narrative_beat(),
            ).compose_factory()
        )

        local_information_factory = LocalInformationFactoryComposer(
            self._playthrough_name
        ).compose_factory()

        player_and_followers_information_factory = (
            RelevantCharactersInformationFactoryComposer(
                self._playthrough_name,
                "Participant",
                ParticipantsIdentifiersStrategy(other_characters_identifiers),
            ).compose_factory()
        )

        narrative_beat_provider_factory = NarrativeBeatProviderFactory(
            produce_tool_response_strategy_factory,
            local_information_factory,
            player_and_followers_information_factory,
        )

        narration_for_dialogue_strategy = NarrativeBeatForDialogueStrategy(
            DialogueManager(self._playthrough_name).load_transcription(),
            narrative_beat_provider_factory,
        )

        web_ambient_narration_observer = WebNarrationObserver()

        return self._process_narration(
            other_characters_identifiers,
            purpose,
            "narrative_beat",
            narration_for_dialogue_strategy,
            web_ambient_narration_observer,
        )

    def process_event_message(
        self,
        other_characters_identifiers: List[str],
        purpose: Optional[str],
        event_text: str,
    ) -> dict:
        web_narration_observer = WebNarrationObserver()

        narration_for_dialogue_strategy = EventNarrationForDialogueStrategy(event_text)

        return self._process_narration(
            other_characters_identifiers,
            purpose,
            "event",
            narration_for_dialogue_strategy,
            web_narration_observer,
        )

    def process_grow_event_message(
        self,
        other_characters_identifiers: List[str],
        purpose: Optional[str],
        event_text: str,
    ):
        web_narration_observer = WebNarrationObserver()

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_grow_event(),
            ).compose_factory()
        )

        local_information_factory = LocalInformationFactoryComposer(
            self._playthrough_name
        ).compose_factory()

        relevant_characters_information_factory = (
            RelevantCharactersInformationFactoryComposer(
                self._playthrough_name,
                "Participant",
                ParticipantsIdentifiersStrategy(other_characters_identifiers),
            ).compose_factory()
        )

        grow_event_provider_factory = GrowEventProviderFactory(
            event_text,
            produce_tool_response_strategy_factory,
            local_information_factory,
            relevant_characters_information_factory,
        )

        grow_event_narration_for_dialogue_strategy = (
            GrowEventNarrationForDialogueStrategy(
                DialogueManager(self._playthrough_name).load_transcription(),
                grow_event_provider_factory,
            )
        )

        return self._process_narration(
            other_characters_identifiers,
            purpose,
            "event",
            grow_event_narration_for_dialogue_strategy,
            web_narration_observer,
        )

    def process_user_input(
        self, user_input, other_characters_identifiers: List[str]
    ) -> (List[Dict], bool):
        participants = Participants()

        load_ongoing_conversation_data_command_factory = (
            LoadOngoingConversationDataCommandFactoryComposer(
                self._playthrough_name, other_characters_identifiers, participants
            ).composer_factory()
        )

        web_player_input_factory = WebPlayerInputFactory(user_input)

        web_dialogue_observer = WebDialogueObserver()

        playthrough_manager = PlaythroughManager(self._playthrough_name)

        # If it turns out that at this point there aren't enough participants,
        # that means that there's no ongoing dialogue. And if there aren't participants in session,
        # we shouldn't have reached this point.
        if not participants.enough_participants():
            DialogueManager(self._playthrough_name).gather_participants_data(
                playthrough_manager.get_player_identifier(),
                session.get("participants"),
                participants,
            )

        setup_command = SetupDialogueCommand(
            self._playthrough_name,
            playthrough_manager.get_player_identifier(),
            participants,
            session.get("purpose", ""),
            web_dialogue_observer,
            web_player_input_factory,
            load_ongoing_conversation_data_command_factory,
            WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(),
            WebMessageDataProducerForSpeechTurnStrategy(
                self._playthrough_name,
                playthrough_manager.get_player_identifier(),
            ),
        )

        player_input_product = web_player_input_factory.create_player_input()

        setup_command.execute()

        is_goodbye = player_input_product.is_goodbye()

        messages = self.prepare_messages(web_dialogue_observer)

        return messages, is_goodbye

    @staticmethod
    def prepare_messages(web_dialogue_observer: WebDialogueObserver) -> List[Dict]:
        messages = []
        for message in web_dialogue_observer.get_messages():
            message["sender_photo_url"] = url_for(
                "static", filename=message["sender_photo_url"]
            )
            messages.append(message)
        return messages

    @staticmethod
    def control_size_of_messages_in_session(dialogue):
        config_loader = ConfigLoader()

        if len(dialogue) > config_loader.get_max_dialogue_entries_for_web():
            dialogue = dialogue[-config_loader.get_max_dialogue_entries_for_web() :]
        session["dialogue"] = dialogue

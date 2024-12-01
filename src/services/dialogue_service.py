import logging
from typing import List, Dict, Optional

from flask import session, url_for

from src.base.playthrough_manager import PlaythroughManager
from src.base.products.texts_product import TextsProduct
from src.base.validators import validate_non_empty_string
from src.characters.composers.local_information_factory_composer import (
    LocalInformationFactoryComposer,
)
from src.characters.composers.relevant_characters_information_factory_composer import (
    RelevantCharactersInformationFactoryComposer,
)
from src.concepts.composers.format_known_facts_algorithm_composer import (
    FormatKnownFactsAlgorithmComposer,
)
from src.dialogues.abstracts.strategies import NarrationForDialogueStrategy
from src.dialogues.composers.produce_dialogue_command_composer import (
    ProduceDialogueCommandComposer,
)
from src.dialogues.composers.produce_narration_for_dialogue_command_composer import (
    ProduceNarrationForDialogueCommandComposer,
)
from src.dialogues.composers.summarize_dialogue_command_factory_composer import (
    SummarizeDialogueCommandFactoryComposer,
)
from src.dialogues.dialogue_manager import DialogueManager
from src.dialogues.factories.ambient_narration_provider_factory import (
    AmbientNarrationProviderFactory,
)
from src.dialogues.factories.confrontation_round_provider_factory import (
    ConfrontationRoundProviderFactory,
)
from src.dialogues.factories.grow_event_provider_factory import GrowEventProviderFactory
from src.dialogues.factories.narrative_beat_provider_factory import (
    NarrativeBeatProviderFactory,
)
from src.dialogues.factories.web_player_input_factory import WebPlayerInputFactory
from src.dialogues.models.brainstormed_events import BrainstormedEvents
from src.dialogues.observers.web_dialogue_observer import WebDialogueObserver
from src.dialogues.observers.web_narration_observer import (
    WebNarrationObserver,
)
from src.dialogues.participants import Participants
from src.dialogues.providers.brainstorm_events_provider import BrainstormEventsProvider
from src.dialogues.repositories.ongoing_dialogue_repository import (
    OngoingDialogueRepository,
)
from src.dialogues.strategies.ambient_narration_for_dialogue_strategy import (
    AmbientNarrationForDialogueStrategy,
)
from src.dialogues.strategies.confrontation_round_for_dialogue_strategy import (
    ConfrontationRoundForDialogueStrategy,
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

        format_known_facts_algorithm = FormatKnownFactsAlgorithmComposer(
            self._playthrough_name
        ).compose_algorithm()

        narrative_beat_provider_factory = NarrativeBeatProviderFactory(
            format_known_facts_algorithm,
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

    def process_confrontation_round(
        self,
        other_characters_identifiers: List[str],
        purpose: Optional[str],
        confrontation_context: str,
    ):
        validate_non_empty_string(confrontation_context, "confrontation_context")

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_confrontation_round(),
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

        format_known_facts_algorithm = FormatKnownFactsAlgorithmComposer(
            self._playthrough_name
        ).compose_algorithm()

        confrontation_round_provider_factory = ConfrontationRoundProviderFactory(
            self._playthrough_name,
            confrontation_context,
            format_known_facts_algorithm,
            produce_tool_response_strategy_factory,
            local_information_factory,
            relevant_characters_information_factory,
        )

        narration_for_dialogue_strategy = ConfrontationRoundForDialogueStrategy(
            DialogueManager(self._playthrough_name).load_transcription(),
            confrontation_round_provider_factory,
        )

        web_ambient_narration_observer = WebNarrationObserver()

        return self._process_narration(
            other_characters_identifiers,
            purpose,
            "confrontation_round",
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

        format_known_facts_algorithm = FormatKnownFactsAlgorithmComposer(
            self._playthrough_name
        ).compose_algorithm()

        grow_event_provider_factory = GrowEventProviderFactory(
            event_text,
            format_known_facts_algorithm,
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

    def process_brainstorm_events(
        self,
        other_characters_identifiers: List[str],
    ) -> TextsProduct:
        transcription = DialogueManager(self._playthrough_name).load_transcription()

        format_known_facts_algorithm = FormatKnownFactsAlgorithmComposer(
            self._playthrough_name
        ).compose_algorithm()

        produce_tool_response_strategy_factory = (
            ProduceToolResponseStrategyFactoryComposer(
                Llms().for_brainstorm_events()
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

        product = BrainstormEventsProvider(
            transcription,
            format_known_facts_algorithm,
            produce_tool_response_strategy_factory,
            local_information_factory,
            relevant_characters_information_factory,
        ).generate_product(BrainstormedEvents)

        return product

    def process_user_input(
        self, user_input, other_characters_identifiers: List[str]
    ) -> (List[Dict], bool):
        participants = Participants()

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

        purpose = session.get("purpose", "")

        web_player_input_factory = WebPlayerInputFactory(user_input)

        player_input_product = web_player_input_factory.create_player_input()

        web_dialogue_observer = WebDialogueObserver()

        produce_dialogue_command = ProduceDialogueCommandComposer(
            self._playthrough_name,
            other_characters_identifiers,
            participants,
            purpose,
            web_dialogue_observer,
            web_player_input_factory,
        ).compose_command()

        produce_dialogue_command.execute()

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
    def remove_participants_from_dialogue(
        playthrough_name: str, selected_characters: List[str]
    ) -> None:
        # Remove selected characters from session participants
        session["participants"] = [
            identifier
            for identifier in session.get("participants", [])
            if identifier not in selected_characters
        ]
        session.modified = True  # Ensure session is saved

        OngoingDialogueRepository(playthrough_name).remove_participants(
            selected_characters
        )

        # Generate summaries for each removed character
        summarize_dialogue_command_factory = SummarizeDialogueCommandFactoryComposer(
            playthrough_name,
            selected_characters,
        ).compose_factory()

        # Load the transcription.
        transcription = DialogueManager(playthrough_name).load_transcription()

        # Create and execute SummarizeDialogueCommand
        summarize_command = (
            summarize_dialogue_command_factory.create_summarize_dialogue_command(
                transcription
            )
        )
        summarize_command.execute()

from typing import Optional

from src.base.abstracts.command import Command
from src.base.abstracts.observer import Observer
from src.characters.factories.store_character_memory_command_factory import (
    StoreCharacterMemoryCommandFactory,
)
from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.strategies import (
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
    MessageDataProducerForSpeechTurnStrategy,
)
from src.dialogues.commands.produce_dialogue_command import ProduceDialogueCommand
from src.dialogues.composers.dialogue_turn_factory_composer import (
    DialogueTurnFactoryComposer,
)
from src.dialogues.factories.dialogue_summary_provider_factory import (
    DialogueSummaryProviderFactory,
)
from src.dialogues.factories.introduce_player_input_into_dialogue_command_factory import (
    IntroducePlayerInputIntoDialogueCommandFactory,
)
from src.dialogues.factories.store_dialogues_command_factory import (
    StoreDialoguesCommandFactory,
)
from src.dialogues.factories.summarize_dialogue_command_factory import (
    SummarizeDialogueCommandFactory,
)
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.participants import Participants
from src.dialogues.strategies.concrete_involve_player_in_dialogue_strategy import (
    ConcreteInvolvePlayerInDialogueStrategy,
)
from src.dialogues.transcription import Transcription
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.llms import Llms


class LaunchDialogueCommand(Command):

    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        participants: Participants,
        purpose: Optional[str],
        messages_to_llm: Optional[MessagesToLlm],
        transcription: Optional[Transcription],
        dialogue_observer: Observer,
        player_input_factory: PlayerInputFactory,
        message_data_producer_for_introduce_player_input_into_dialogue_strategy: MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
        message_data_producer_for_speech_turn_strategy: MessageDataProducerForSpeechTurnStrategy,
        llms: Optional[Llms] = None,
    ):
        if not participants.enough_participants():
            raise ValueError("Not enough participants.")
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._participants = participants
        self._purpose = purpose
        self._messages_to_llm = messages_to_llm
        self._transcription = transcription
        self._dialogue_observer = dialogue_observer
        self._player_input_factory = player_input_factory
        (
            self._message_data_producer_for_introduce_player_input_into_dialogue_strategy
        ) = message_data_producer_for_introduce_player_input_into_dialogue_strategy
        self._message_data_producer_for_speech_turn_strategy = (
            message_data_producer_for_speech_turn_strategy
        )
        self._llms = llms or Llms()

    def execute(self) -> None:
        introduce_player_input_into_dialogue_command_factory = IntroducePlayerInputIntoDialogueCommandFactory(
            self._playthrough_name,
            self._player_identifier,
            self._message_data_producer_for_introduce_player_input_into_dialogue_strategy,
        )
        llm_client = OpenRouterLlmClientFactory().create_llm_client()
        involve_player_in_dialogue_strategy = ConcreteInvolvePlayerInDialogueStrategy(
            self._player_identifier,
            self._player_input_factory,
            introduce_player_input_into_dialogue_command_factory,
        )
        dialogue_turn_factory = DialogueTurnFactoryComposer(
            self._playthrough_name,
            self._player_identifier,
            self._participants,
            self._purpose,
            llm_client,
            self._messages_to_llm,
            self._transcription,
            involve_player_in_dialogue_strategy,
            self._message_data_producer_for_speech_turn_strategy,
        ).compose()
        dialogue_turn_factory.attach(self._dialogue_observer)
        dialogue_summary_provider_factory = DialogueSummaryProviderFactory(
            llm_client, self._llms.for_dialogue_summary()
        )
        store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(
            self._playthrough_name
        )
        summarize_dialogue_command_factory = SummarizeDialogueCommandFactory(
            self._participants,
            dialogue_summary_provider_factory,
            store_character_memory_command_factory,
        )
        store_dialogues_command_factory = StoreDialoguesCommandFactory(
            self._playthrough_name, self._participants
        )
        produce_dialogue_command = ProduceDialogueCommand(
            self._playthrough_name,
            self._participants,
            self._purpose,
            dialogue_turn_factory,
            summarize_dialogue_command_factory,
            store_dialogues_command_factory,
        )
        involve_player_in_dialogue_strategy.attach(self._dialogue_observer)
        produce_dialogue_command.execute()

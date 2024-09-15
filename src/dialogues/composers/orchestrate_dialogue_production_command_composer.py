from src.abstracts.observer import Observer
from src.characters.factories.store_character_memory_command_factory import StoreCharacterMemoryCommandFactory
from src.dialogues.abstracts.abstract_factories import DialogueFactorySubject
from src.dialogues.abstracts.protocols import InvolvePlayerInDialogueStrategySubject
from src.dialogues.commands.orchestrate_dialogue_production_command import OrchestrateDialogueProductionCommand
from src.dialogues.commands.produce_dialogue_command import ProduceDialogueCommand
from src.dialogues.factories.dialogue_summary_provider_factory import DialogueSummaryProviderFactory
from src.dialogues.factories.store_dialogues_command_factory import StoreDialoguesCommandFactory
from src.dialogues.factories.summarize_dialogue_command_factory import SummarizeDialogueCommandFactory
from src.dialogues.participants import Participants
from src.prompting.abstracts.llm_client import LlmClient


class OrchestrateDialogueProductionCommandComposer:
    def __init__(self, playthrough_name: str, participants: Participants, llm_client: LlmClient, model: str,
                 dialogue_observer: Observer,
                 involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategySubject,
                 dialogue_factory: DialogueFactorySubject):
        if not playthrough_name:
            raise ValueError("playthrough_name must not be empty.")
        if not participants.enough_participants():
            raise ValueError("There must be at least two participants in the dialogue.")
        if not model:
            raise ValueError("model must not be empty.")

        self._playthrough_name = playthrough_name
        self._participants = participants
        self._llm_client = llm_client
        self._model = model
        self._dialogue_observer = dialogue_observer
        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy
        self._dialogue_factory = dialogue_factory

    def compose(self) -> OrchestrateDialogueProductionCommand:
        dialogue_summary_provider_factory = DialogueSummaryProviderFactory(self._llm_client, self._model)

        store_character_memory_command_factory = StoreCharacterMemoryCommandFactory(self._playthrough_name)

        summarize_dialogue_command_factory = SummarizeDialogueCommandFactory(self._participants,
                                                                             dialogue_summary_provider_factory,
                                                                             store_character_memory_command_factory)

        store_dialogues_command_factory = StoreDialoguesCommandFactory(self._playthrough_name, self._participants)

        produce_dialogue_command = ProduceDialogueCommand(self._playthrough_name, self._participants,
                                                          self._dialogue_factory,
                                                          summarize_dialogue_command_factory,
                                                          store_dialogues_command_factory)

        return OrchestrateDialogueProductionCommand(self._involve_player_in_dialogue_strategy, self._dialogue_factory,
                                                    self._dialogue_observer,
                                                    produce_dialogue_command)

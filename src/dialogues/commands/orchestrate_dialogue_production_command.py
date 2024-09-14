from src.abstracts.command import Command
from src.abstracts.observer import Observer
from src.dialogues.abstracts.abstract_factories import DialogueFactorySubject
from src.dialogues.abstracts.protocols import InvolvePlayerInDialogueStrategySubject
from src.dialogues.commands.produce_dialogue_command import ProduceDialogueCommand


class OrchestrateDialogueProductionCommand(Command):
    def __init__(self, involve_player_in_dialogue_strategy: InvolvePlayerInDialogueStrategySubject,
                 dialogue_factory: DialogueFactorySubject,
                 dialogue_observer: Observer, produce_dialogue_command: ProduceDialogueCommand):
        if not involve_player_in_dialogue_strategy:
            raise ValueError("involve_player_in_dialogue_strategy can't be empty.")
        if not dialogue_factory:
            raise ValueError("dialogue_factory can't be empty.")
        if not dialogue_observer:
            raise ValueError("dialogue_observer can't be empty.")
        if not produce_dialogue_command:
            raise ValueError("produce_dialogue_command can't be empty.")

        self._involve_player_in_dialogue_strategy = involve_player_in_dialogue_strategy
        self._dialogue_factory = dialogue_factory
        self._dialogue_observer = dialogue_observer
        self._produce_dialogue_command = produce_dialogue_command

    def execute(self) -> None:
        self._involve_player_in_dialogue_strategy.attach(self._dialogue_observer)

        self._dialogue_factory.attach(self._dialogue_observer)

        self._produce_dialogue_command.execute()

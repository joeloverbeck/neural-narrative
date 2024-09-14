from src.abstracts.command import Command
from src.dialogues.abstracts.abstract_factories import DialogueFactory
from src.dialogues.factories.store_dialogues_command_factory import StoreDialoguesCommandFactory
from src.dialogues.factories.summarize_dialogue_command_factory import SummarizeDialogueCommandFactory


class ProduceDialogueCommand(Command):
    def __init__(self, dialogue_factory: DialogueFactory,
                 summarize_dialogue_command_factory: SummarizeDialogueCommandFactory,
                 store_dialogues_command_factory: StoreDialoguesCommandFactory):
        self._dialogue_factory = dialogue_factory
        self._summarize_dialogue_command_factory = summarize_dialogue_command_factory
        self._store_dialogues_command_factory = store_dialogues_command_factory

    def execute(self) -> None:
        dialogue_product = self._dialogue_factory.create_dialogue()

        self._summarize_dialogue_command_factory.create_summarize_dialogue_command(
            dialogue_product.get()).execute()

        self._store_dialogues_command_factory.create_store_dialogues_command(dialogue_product.get()).execute()

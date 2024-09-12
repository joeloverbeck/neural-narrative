from typing import List

from openai import OpenAI

from src.abstracts.command import Command
from src.characters.commands.store_character_memory_command import StoreCharacterMemoryCommand
from src.dialogues.factories.concrete_dialogue_summary_factory import ConcreteDialogueSummaryFactory


class SummarizeDialogueCommand(Command):

    def __init__(self, playthrough_name: str, client: OpenAI, model: str, participants: List[int],
                 dialogue: List[str]):
        assert playthrough_name
        assert client
        assert model
        assert len(participants) >= 2

        self._playthrough_name = playthrough_name
        self._client = client
        self._model = model
        self._participants = participants
        self._dialogue = dialogue

    def execute(self) -> None:
        # Once the chat is over, the LLM should be prompted to create a memory out of it for all participants.
        if not self._dialogue or len(self._dialogue) <= 4:
            # Perhaps the dialogue is empty. In that case, no summary needs to be done.
            print("Won't create memories out of an empty dialogue or insufficient dialogue.")
            return

        summary_product = ConcreteDialogueSummaryFactory(self._client, self._model, self._dialogue).create_summary()

        if not summary_product.is_valid():
            raise ValueError(f"Failed to create a summary for the dialogue: {summary_product.get_error()}")

        # Now that we have the summary, gotta add it to the memories of all participants.
        for participant_identifier in self._participants:
            StoreCharacterMemoryCommand(self._playthrough_name, participant_identifier, summary_product.get()).execute()

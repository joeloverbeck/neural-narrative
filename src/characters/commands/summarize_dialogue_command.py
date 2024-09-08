from typing import List, Any

from openai import OpenAI

from src.abstracts.command import Command
from src.characters.commands.store_character_memory import StoreCharacterMemory
from src.constants import SUMMARIZE_DIALOGUE_PROMPT_FILE, DIALOGUE_SUMMARIZATION_TOOL_FILE, TOOL_INSTRUCTIONS_FILE
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.factories.concrete_ai_completion_factory import ConcreteAiCompletionFactory
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.dialogue_summary_tool_response_data_extraction_factory import \
    DialogueSummaryToolResponseDataExtractionFactory
from src.prompting.factories.open_ai_llm_content_factory import OpenAiLlmContentFactory
from src.tools import generate_tool_prompt


class SummarizeDialogueCommand(Command):

    def __init__(self, playthrough_name: str, client: OpenAI, model: str, participants: List[int],
                 dialogue: List[dict[Any, str]]):
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

        filesystem_manager = FilesystemManager()

        messages = [
            {
                "role": "system",
                "content": filesystem_manager.read_file(
                    SUMMARIZE_DIALOGUE_PROMPT_FILE) + f"\n\nHere's the dialogue to summarize:\n{self._dialogue}" + generate_tool_prompt(
                    filesystem_manager.read_json_file(DIALOGUE_SUMMARIZATION_TOOL_FILE),
                    filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE)),
            },
            {
                "role": "user",
                "content": "Summarize the provided dialogue. Do not write any preamble, just do it as instructed."
            }
        ]

        # Now prompt the LLM for a response.
        llm_content_product = OpenAiLlmContentFactory(client=self._client, model=self._model,
                                                      messages=messages,
                                                      ai_completion_factory=ConcreteAiCompletionFactory(
                                                          self._client)).generate_content()

        if llm_content_product.is_valid():
            tool_response_parsing_product = ConcreteToolResponseParsingFactory(
                llm_content_product.get()).parse_tool_response()

            if not tool_response_parsing_product.is_valid():
                raise ValueError(
                    f"Failed to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}")

            summary = DialogueSummaryToolResponseDataExtractionFactory(
                tool_response_parsing_product.get()).extract_data().get()

            # Now that we have the summary, gotta add it to the memories of all participants.
            for participant_identifier in self._participants:
                StoreCharacterMemory(self._playthrough_name, participant_identifier, summary).execute()
        else:
            raise ValueError(f"Failed to summarize dialogue: {llm_content_product.get_error()}")

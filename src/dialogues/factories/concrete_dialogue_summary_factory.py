from typing import List

from src.constants import SUMMARIZE_DIALOGUE_PROMPT_FILE, DIALOGUE_SUMMARIZATION_TOOL_FILE, TOOL_INSTRUCTIONS_FILE, \
    MAX_RETRIES
from src.dialogues.abstracts.abstract_factories import DialogueSummaryFactory
from src.dialogues.abstracts.factory_products import SummaryProduct
from src.dialogues.products.concrete_summary_product import ConcreteSummaryProduct
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.factories.concrete_llm_content_factory import ConcreteLlmContentFactory
from src.prompting.factories.concrete_tool_response_parsing_factory import ConcreteToolResponseParsingFactory
from src.prompting.factories.dialogue_summary_tool_response_data_extraction_factory import \
    DialogueSummaryToolResponseDataExtractionFactory
from src.tools import generate_tool_prompt


class ConcreteDialogueSummaryFactory(DialogueSummaryFactory):
    def __init__(self, llm_client: LlmClient, model: str, dialogue: List[str], max_retries: int = MAX_RETRIES):
        assert llm_client
        assert model
        assert dialogue

        self._llm_client = llm_client
        self._model = model
        self._dialogue = dialogue
        self._max_retries = max_retries

    def create_summary(self) -> SummaryProduct:
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
        llm_content_product = ConcreteLlmContentFactory(model=self._model, messages=messages,
                                                        llm_client=self._llm_client,
                                                        max_retries=self._max_retries,
                                                        temperature=0.2).generate_content()

        if not llm_content_product.is_valid():
            return ConcreteSummaryProduct("", is_valid=False,
                                          error=f"The LLM failed to produce valid content: {llm_content_product.get_error()}")

        # At this point, the large language model's content is valid, but we need to know if the tool response can properly be parsed.
        tool_response_parsing_product = ConcreteToolResponseParsingFactory(
            llm_content_product.get()).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            return ConcreteSummaryProduct("", is_valid=False,
                                          error=f"Failed to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}")

        return ConcreteSummaryProduct(DialogueSummaryToolResponseDataExtractionFactory(
            tool_response_parsing_product.get()).extract_data().get(), is_valid=True)

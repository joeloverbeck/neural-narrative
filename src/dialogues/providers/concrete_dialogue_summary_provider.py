from src.constants import (
    SUMMARIZE_DIALOGUE_PROMPT_FILE,
    DIALOGUE_SUMMARIZATION_TOOL_FILE,
    TOOL_INSTRUCTIONS_FILE,
    MAX_RETRIES,
)
from src.dialogues.abstracts.abstract_factories import DialogueSummaryProvider
from src.dialogues.abstracts.factory_products import SummaryProduct
from src.dialogues.messages_to_llm import MessagesToLlm
from src.dialogues.products.concrete_summary_product import ConcreteSummaryProduct
from src.dialogues.transcription import Transcription
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.llm_client import LlmClient
from src.prompting.factories.dialogue_summary_tool_response_data_extraction_factory import (
    DialogueSummaryToolResponseDataExtractionFactory,
)
from src.prompting.providers.concrete_llm_content_provider import (
    ConcreteLlmContentProvider,
)
from src.prompting.providers.concrete_tool_response_parsing_provider import (
    ConcreteToolResponseParsingProvider,
)
from src.tools import generate_tool_prompt


class ConcreteDialogueSummaryProvider(DialogueSummaryProvider):
    def __init__(
        self,
        llm_client: LlmClient,
        model: str,
        transcription: Transcription,
        max_retries: int = MAX_RETRIES,
    ):
        assert llm_client
        assert model
        if not transcription:
            raise ValueError("transcription must not be empty.")

        self._llm_client = llm_client
        self._model = model
        self._transcription = transcription
        self._max_retries = max_retries

    def create_summary(self) -> SummaryProduct:
        filesystem_manager = FilesystemManager()

        messages_to_llm = MessagesToLlm()
        messages_to_llm.add_message(
            "system",
            filesystem_manager.read_file(SUMMARIZE_DIALOGUE_PROMPT_FILE)
            + f"\n\nHere's the dialogue to summarize:\n{self._transcription.get_prettified_transcription()}"
            + generate_tool_prompt(
                filesystem_manager.read_json_file(DIALOGUE_SUMMARIZATION_TOOL_FILE),
                filesystem_manager.read_file(TOOL_INSTRUCTIONS_FILE),
            ),
        )
        messages_to_llm.add_message(
            "user",
            "Summarize the provided dialogue. Do not write any preamble, just do it as instructed.",
        )

        # Now prompt the LLM for a response.
        llm_content_product = ConcreteLlmContentProvider(
            model=self._model,
            messages_to_llm=messages_to_llm,
            llm_client=self._llm_client,
            max_retries=self._max_retries,
            temperature=0.2,
        ).generate_content()

        if not llm_content_product.is_valid():
            return ConcreteSummaryProduct(
                "",
                is_valid=False,
                error=f"The LLM failed to produce valid content: {llm_content_product.get_error()}",
            )

        # At this point, the large language model's content is valid, but we need to know if the tool response can properly be parsed.
        tool_response_parsing_product = ConcreteToolResponseParsingProvider(
            llm_content_product.get()
        ).parse_tool_response()

        if not tool_response_parsing_product.is_valid():
            return ConcreteSummaryProduct(
                "",
                is_valid=False,
                error=f"Failed to parse the tool response from the LLM: {tool_response_parsing_product.get_error()}",
            )

        return ConcreteSummaryProduct(
            DialogueSummaryToolResponseDataExtractionFactory(
                tool_response_parsing_product.get()
            )
            .extract_data()
            .get(),
            is_valid=True,
        )

from typing import Optional, Type

from pydantic import BaseModel

from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.enums import LlmClientType
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)
from src.prompting.factories.instructor_llm_client_factory import (
    InstructorLlmClientFactory,
)
from src.prompting.factories.llm_content_provider_factory import (
    LlmContentProviderFactory,
)
from src.prompting.factories.openrouter_llm_client_factory import (
    OpenRouterLlmClientFactory,
)
from src.prompting.factories.tool_response_parsing_provider_factory import (
    ToolResponseParsingProviderFactory,
)
from src.prompting.factories.unparsed_string_produce_tool_response_strategy_factory import (
    UnparsedStringProduceToolResponseStrategyFactory,
)


class ProduceToolResponseStrategyFactoryComposer:
    def __init__(
        self,
        llm_client_type: LlmClientType,
        model: str,
        response_model: Optional[Type[BaseModel]] = None,
    ):
        self._llm_client_type = llm_client_type
        self._model = model
        self._response_model = response_model

    def compose_factory(self) -> ProduceToolResponseStrategyFactory:
        if self._llm_client_type == LlmClientType.OPEN_ROUTER:
            llm_content_provider_factory = LlmContentProviderFactory(
                OpenRouterLlmClientFactory().create_llm_client(),
                self._model,
            )

            tool_response_parsing_provider_factory = (
                ToolResponseParsingProviderFactory()
            )

            return UnparsedStringProduceToolResponseStrategyFactory(
                llm_content_provider_factory, tool_response_parsing_provider_factory
            )
        else:
            llm_content_provider_factory = LlmContentProviderFactory(
                InstructorLlmClientFactory(self._response_model).create_llm_client(),
                self._model,
            )

            return BaseModelProduceToolResponseStrategyFactory(
                llm_content_provider_factory
            )

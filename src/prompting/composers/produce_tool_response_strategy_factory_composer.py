from src.prompting.abstracts.abstract_factories import (
    ProduceToolResponseStrategyFactory,
)
from src.prompting.factories.base_model_produce_tool_response_strategy_factory import (
    BaseModelProduceToolResponseStrategyFactory,
)
from src.prompting.factories.instructor_llm_client_factory import (
    InstructorLlmClientFactory,
)
from src.prompting.factories.llm_content_provider_factory import (
    LlmContentProviderFactory,
)


class ProduceToolResponseStrategyFactoryComposer:
    def __init__(
        self,
        model: str,
    ):
        self._model = model

    def compose_factory(self) -> ProduceToolResponseStrategyFactory:
        llm_content_provider_factory = LlmContentProviderFactory(
            InstructorLlmClientFactory(),
            self._model,
        )

        return BaseModelProduceToolResponseStrategyFactory(llm_content_provider_factory)

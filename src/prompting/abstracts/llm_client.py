from abc import ABC, abstractmethod
from typing import List

from src.prompting.abstracts.factory_products import AiCompletionProduct


class LlmClient(ABC):
    @abstractmethod
    def generate_completion(self, model: str, messages: List[dict], temperature=1.0, top_p=1.0) -> AiCompletionProduct:
        pass

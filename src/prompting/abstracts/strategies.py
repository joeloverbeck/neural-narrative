from abc import ABC, abstractmethod


class ProduceToolResponseStrategy(ABC):

    @abstractmethod
    def produce_tool_response(self, system_content: str, user_content: str) -> dict:
        pass

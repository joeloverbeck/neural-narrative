from abc import ABC, abstractmethod

from src.base.required_string import RequiredString


class ProduceToolResponseStrategy(ABC):
    @abstractmethod
    def produce_tool_response(
        self, system_content: RequiredString, user_content: RequiredString
    ) -> dict:
        pass

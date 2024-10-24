from abc import ABC, abstractmethod
from typing import Union, Type

from pydantic import BaseModel


class ProduceToolResponseStrategy(ABC):

    @abstractmethod
    def produce_tool_response(
        self, system_content: str, user_content: str, response_model: Type[BaseModel]
    ) -> Union[dict, BaseModel]:
        pass

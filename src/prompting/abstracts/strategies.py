from abc import ABC, abstractmethod
from typing import Union

from pydantic import BaseModel


class ProduceToolResponseStrategy(ABC):

    @abstractmethod
    def produce_tool_response(
        self, system_content: str, user_content: str
    ) -> Union[dict, BaseModel]:
        pass

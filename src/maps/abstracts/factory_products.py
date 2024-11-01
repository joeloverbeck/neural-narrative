from typing import Protocol

from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType


class RandomTemplateTypeMapEntryCreationResult(Protocol):

    def get_result_type(self) -> RandomTemplateTypeMapEntryCreationResultType:
        pass

    def get_error(self) -> str:
        pass


class CardinalConnectionCreationProduct(Protocol):

    def was_successful(self) -> bool:
        pass

    def get_error(self) -> str:
        pass

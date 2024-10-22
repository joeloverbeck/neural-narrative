from src.maps.abstracts.factory_products import RandomTemplateTypeMapEntryCreationResult
from src.maps.enums import RandomTemplateTypeMapEntryCreationResultType


class ConcreteRandomTemplateTypeMapEntryCreationResult(
    RandomTemplateTypeMapEntryCreationResult):

    def __init__(self, random_place_type_map_entry_creation_result_type:
    RandomTemplateTypeMapEntryCreationResultType, error: str = None):
        self._random_place_type_map_entry_creation_result_type = (
            random_place_type_map_entry_creation_result_type)
        self._error = error

    def get_result_type(self) -> RandomTemplateTypeMapEntryCreationResultType:
        return self._random_place_type_map_entry_creation_result_type

    def get_error(self) -> str:
        return self._error

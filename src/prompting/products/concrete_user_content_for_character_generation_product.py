from src.prompting.abstracts.factory_products import UserContentForCharacterGenerationProduct


class ConcreteUserContentForCharacterGenerationProduct(UserContentForCharacterGenerationProduct):
    def __init__(self, user_content_for_character_generation: str, is_valid: bool, error: str = None):
        self._user_content_for_character_generation = user_content_for_character_generation
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._user_content_for_character_generation

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error

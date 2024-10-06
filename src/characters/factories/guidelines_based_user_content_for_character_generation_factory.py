from src.prompting.abstracts.abstract_factories import (
    UserContentForCharacterGenerationFactory,
)
from src.prompting.abstracts.factory_products import (
    UserContentForCharacterGenerationProduct,
)
from src.prompting.products.concrete_user_content_for_character_generation_product import (
    ConcreteUserContentForCharacterGenerationProduct,
)


class GuidelinesBasedUserContentForCharacterGenerationFactory(
    UserContentForCharacterGenerationFactory
):
    def __init__(self, guideline: str):
        if not guideline:
            raise ValueError("guideline can't be empty.")

        self._guideline = guideline

    def create_user_content_for_character_generation(
        self,
    ) -> UserContentForCharacterGenerationProduct:
        return ConcreteUserContentForCharacterGenerationProduct(
            f"Create the bio for a character influenced by the places described above, as well as the following guideline: {self._guideline}",
            is_valid=True,
        )

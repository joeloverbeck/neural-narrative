from src.prompting.abstracts.abstract_factories import (
    UserContentForCharacterGenerationFactory,
)
from src.prompting.abstracts.factory_products import (
    UserContentForCharacterGenerationProduct,
)
from src.prompting.products.concrete_user_content_for_character_generation_product import (
    ConcreteUserContentForCharacterGenerationProduct,
)


class PlayerGuidedUserContentForCharacterGenerationFactory(
    UserContentForCharacterGenerationFactory
):
    def __init__(self, user_content: str):
        if not user_content:
            raise ValueError("user_content can't be empty.")

        self._user_content = user_content

    def create_user_content_for_character_generation(
        self,
    ) -> UserContentForCharacterGenerationProduct:
        return ConcreteUserContentForCharacterGenerationProduct(
            f"Create the bio for a character influenced by the places described above, as well as the following notions provided by the user: {self._user_content}",
            is_valid=True,
        )

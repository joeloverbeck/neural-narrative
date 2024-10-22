from src.prompting.abstracts.abstract_factories import UserContentForCharacterGenerationFactory
from src.prompting.abstracts.factory_products import UserContentForCharacterGenerationProduct
from src.prompting.products.concrete_user_content_for_character_generation_product import \
    ConcreteUserContentForCharacterGenerationProduct


class AutomaticUserContentForCharacterGenerationFactory(
    UserContentForCharacterGenerationFactory):

    def create_user_content_for_character_generation(self
                                                     ) -> UserContentForCharacterGenerationProduct:
        return ConcreteUserContentForCharacterGenerationProduct(
            f'Create the bio for a character influenced by the places described above.'
            , is_valid=True)

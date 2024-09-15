from src.interfaces.console_interface_manager import ConsoleInterfaceManager
from src.prompting.abstracts.abstract_factories import UserContentForCharacterGenerationFactory
from src.prompting.abstracts.factory_products import UserContentForCharacterGenerationProduct
from src.prompting.products.concrete_user_content_for_character_generation_product import \
    ConcreteUserContentForCharacterGenerationProduct


class PlayerGuidedUserContentForCharacterGenerationFactory(UserContentForCharacterGenerationFactory):
    def create_user_content_for_character_generation(self) -> UserContentForCharacterGenerationProduct:
        user_content = ConsoleInterfaceManager().prompt_for_input("What kind of character do you want to be?: ")

        return ConcreteUserContentForCharacterGenerationProduct(
            f"Create the bio for a character influenced by the places described above, as well as the following notions provided by the user: {user_content}",
            is_valid=True)

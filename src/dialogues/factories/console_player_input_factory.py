from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.products.concrete_player_input_product import ConcretePlayerInputProduct


class ConsolePlayerInputFactory(PlayerInputFactory):
    def create_player_input(self) -> PlayerInputProduct:
        return ConcretePlayerInputProduct(input("\nYour input [options: goodbye, silent]: "))

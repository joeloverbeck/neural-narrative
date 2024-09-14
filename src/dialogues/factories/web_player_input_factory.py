from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.products.concrete_player_input_product import ConcretePlayerInputProduct


class WebPlayerInputFactory(PlayerInputFactory):
    def __init__(self, user_input: str):
        self.user_input = user_input

    def create_player_input(self) -> PlayerInputProduct:
        return ConcretePlayerInputProduct(self.user_input)

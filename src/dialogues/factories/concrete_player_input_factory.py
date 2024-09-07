from src.dialogues.abstracts.abstract_factories import PlayerInputFactory
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.products.concrete_player_input_product import ConcretePlayerInputProduct


class ConcretePlayerInputFactory(PlayerInputFactory):
    def __init__(self, system_prompt: str):
        self._system_prompt = system_prompt

    def create_player_input(self) -> PlayerInputProduct:
        return ConcretePlayerInputProduct(input(self._system_prompt))

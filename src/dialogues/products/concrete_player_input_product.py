from src.dialogues.abstracts.factory_products import PlayerInputProduct


class ConcretePlayerInputProduct(PlayerInputProduct):
    def __init__(self, player_input: str):
        self._player_input = player_input

    def get(self) -> str:
        return self._player_input

    def is_goodbye(self) -> bool:
        return self._player_input.lower() == "goodbye"

    def is_quit(self) -> bool:
        return self._player_input.lower() == "quit"

    def is_silent(self) -> bool:
        return self._player_input.lower() == "silent"

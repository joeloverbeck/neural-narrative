from typing import Optional
from src.characters.character import Character
from src.characters.characters_manager import CharactersManager
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import DetermineUserMessagesForSpeechTurnStrategy
from src.dialogues.messages_to_llm import MessagesToLlm
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class ConcreteDetermineUserMessagesForSpeechTurnStrategy(
    DetermineUserMessagesForSpeechTurnStrategy):

    def __init__(self, playthrough_name: str, player_identifier: Optional[
        str], player_input_product: PlayerInputProduct, messages_to_llm:
    MessagesToLlm, characters_manager: CharactersManager = None):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._player_input_product = player_input_product
        self._messages_to_llm = messages_to_llm
        self._characters_manager = characters_manager or CharactersManager(self
                                                                           ._playthrough_name)

    def do_algorithm(self, speech_turn_tool_response_product:
    LlmToolResponseProduct):
        if not self._player_identifier or self._player_input_product.is_silent(
        ):
            self._messages_to_llm.add_message('user',
                                              f"Produce {speech_turn_tool_response_product.get()['name']}'s speech."
                                              )
        else:
            self._messages_to_llm.add_message('user',
                                              f'{Character(self._playthrough_name, self._player_identifier).name}: {self._player_input_product.get()}'
                                              )
            self._messages_to_llm.add_message('user',
                                              f"Next, write {speech_turn_tool_response_product.get()['name']}'s speech."
                                              )

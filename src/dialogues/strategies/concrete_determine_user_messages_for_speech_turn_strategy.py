from typing import Optional, List

from src.characters.characters import load_character_data
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import DetermineUserMessagesForSpeechTurnStrategy
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class ConcreteDetermineUserMessagesForSpeechTurnStrategy(DetermineUserMessagesForSpeechTurnStrategy):
    def __init__(self, playthrough_name: str, player_identifier: Optional[int],
                 player_input_product: PlayerInputProduct, previous_messages: List[dict]):
        assert playthrough_name
        assert player_input_product

        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._player_input_product = player_input_product
        self._previous_messages = previous_messages

    def do_algorithm(self, speech_turn_tool_response_product: LlmToolResponseProduct):
        # In case there's no player present, or has remained silent, a 'user' prompt
        # should be appended to the ongoing messages. Otherwise, the LLM won't answer anything.
        if not self._player_identifier or self._player_input_product.is_silent():
            # Should prompt the LLM to speak given the chosen next character.
            self._previous_messages.append(
                {"role": "user", "content": f"Produce {speech_turn_tool_response_product.get()["name"]}'s speech."})
        else:
            self._previous_messages.append(
                {"role": "user",
                 "content": f"{load_character_data(self._playthrough_name, self._player_identifier)["name"]}: {self._player_input_product.get()}"})
            self._previous_messages.append({
                "role": "user",
                "content": f"Next, write {speech_turn_tool_response_product.get()["name"]}'s speech."
            })

from src.characters.character import Character
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import (
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)


class ConsoleMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy
):
    def produce_message_data(
        self, player_character: Character, player_input_product: PlayerInputProduct
    ) -> dict:
        return {
            "name": f"{player_character.name}",
            "speech": f"{player_input_product.get()}",
            "narration_text": "",
        }

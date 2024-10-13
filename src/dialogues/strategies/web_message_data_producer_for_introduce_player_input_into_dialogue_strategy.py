from src.characters.character import Character
from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import (
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)


class WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy
):
    def produce_message_data(
        self, player_character: Character, player_input_product: PlayerInputProduct
    ) -> dict:
        return {
            "alignment": "right",
            "sender_name": player_character.name,
            "sender_photo_url": player_character.image_url,
            "message_text": player_input_product.get(),
            "voice_model": player_character.voice_model,
        }

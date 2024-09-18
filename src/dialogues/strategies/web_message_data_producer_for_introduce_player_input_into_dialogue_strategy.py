from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import (
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy,
)


class WebMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy
):
    def produce_message_data(
            self, player_character_data: dict, player_input_product: PlayerInputProduct
    ) -> dict:
        return {
            "alignment": "right",
            "sender_name": player_character_data["name"],
            "sender_photo_url": player_character_data["image_url"],
            "message_text": player_input_product.get(),
        }

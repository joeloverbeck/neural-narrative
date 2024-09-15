from src.dialogues.abstracts.factory_products import PlayerInputProduct
from src.dialogues.abstracts.strategies import MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy


class ConsoleMessageDataProducerForIntroducePlayerInputIntoDialogueStrategy(
    MessageDataProducerForIntroducePlayerInputIntoDialogueStrategy):
    def produce_message_data(self, player_character_data: dict, player_input_product: PlayerInputProduct) -> dict:
        return {"name": f"{player_character_data["name"]}",
                "speech": f"{player_input_product.get()}",
                "narration_text": ""}

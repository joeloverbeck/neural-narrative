from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct


class WebMessageDataProducerForSpeechTurnStrategy(
    MessageDataProducerForSpeechTurnStrategy
):
    def __init__(
        self,
        playthrough_name: str,
        player_identifier: str,
        filesystem_manager: FilesystemManager = None,
    ):
        self._playthrough_name = playthrough_name
        self._player_identifier = player_identifier
        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def produce_message_data(
        self,
        speech_turn_choice_tool_response_product: LlmToolResponseProduct,
        speech_data_product: SpeechDataProduct,
    ) -> dict[str, str]:
        image_url = self._filesystem_manager.get_file_path_to_character_image_for_web(
            self._playthrough_name,
            speech_turn_choice_tool_response_product.get()["identifier"],
        )
        # Could be that the AI has produced by "mistake" text spoken by the player. It's very notorious in the web version.
        alignment = "left"  # for other characters

        if (
            self._player_identifier
            == speech_turn_choice_tool_response_product.get()["identifier"]
        ):
            alignment = "right"

        name = speech_data_product.get()["name"]
        narration_text = speech_data_product.get()["narration_text"]

        return {
            "alignment": alignment,
            "sender_name": name,
            "sender_photo_url": image_url,
            "message_text": f"*{narration_text}* {speech_data_product.get()['speech']} ",
        }

import logging

from src.dialogues.abstracts.factory_products import SpeechDataProduct
from src.dialogues.abstracts.strategies import MessageDataProducerForSpeechTurnStrategy
from src.dialogues.utils import format_speech
from src.filesystem.filesystem_manager import FilesystemManager
from src.prompting.abstracts.factory_products import LlmToolResponseProduct

logger = logging.getLogger(__name__)


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
        if not "voice_model" in speech_turn_choice_tool_response_product.get():
            raise ValueError(
                "voice_model should be in the speech turn choice response."
            )

        speaker_identifier = speech_turn_choice_tool_response_product.get()[
            "identifier"
        ]

        image_url = self._filesystem_manager.get_file_path_to_character_image_for_web(
            self._playthrough_name,
            speaker_identifier,
        )
        alignment = "left"
        speaker_identifier = speech_turn_choice_tool_response_product.get()[
            "identifier"
        ]

        if self._player_identifier == speaker_identifier:
            alignment = "right"

        name = speech_data_product.get()["name"]
        narration_text = speech_data_product.get()["narration_text"]
        voice_model = speech_turn_choice_tool_response_product.get()["voice_model"]
        thoughts = speech_data_product.get()["thoughts"]
        desired_action = speech_data_product.get()["desired_action"]

        return {
            "alignment": alignment,
            "sender_identifier": speaker_identifier,
            "sender_name": name,
            "sender_photo_url": image_url,
            "message_text": format_speech(
                narration_text, speech_data_product.get()["speech"]
            ),
            "thoughts": thoughts,
            "desired_action": desired_action,
            "voice_model": voice_model,
        }

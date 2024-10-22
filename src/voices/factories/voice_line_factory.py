import io
import logging
import time
import requests
from src.voices.products.voice_line_product import VoiceLineProduct

logger = logging.getLogger(__name__)


class VoiceLineFactory:

    def __init__(self, text: str, voice_model: str, xtts_url: str):
        if not text:
            raise ValueError("text can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")
        if not xtts_url:
            raise ValueError("xtts_url can't be empty.")
        self._text = " " + text + " "
        self._voice_model = voice_model
        self._xtts_url = xtts_url

    def create_voice_line(self) -> VoiceLineProduct:
        payload = {
            "text": self._text,
            "speaker_wav": self._voice_model,
            "language": "en",
            "accent": "en",
        }
        start_time = time.time()
        response = requests.post(self._xtts_url, json=payload)
        if response and response.status_code == 200:
            audio_data = VoiceLineProduct(io.BytesIO(response.content), is_valid=True)
            logging.info(
                f"The voice data took {time.time() - start_time} seconds to generate."
            )
            return audio_data
        else:
            return VoiceLineProduct(
                None,
                False,
                f"Failed with '{self._voice_model}'. HTTP Error: {response.status_code}",
            )

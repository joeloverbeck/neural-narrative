import io

import requests

from src.voices.products.voice_line_product import VoiceLineProduct


class VoiceLineFactory:
    def __init__(self, text: str, voice_model: str, xtts_url: str):
        if not text:
            raise ValueError("text can't be empty.")
        if not voice_model:
            raise ValueError("voice_model can't be empty.")
        if not xtts_url:
            raise ValueError("xtts_url can't be empty.")

        self._text = text
        self._voice_model = voice_model
        self._xtts_url = xtts_url

    def create_voice_line(self) -> VoiceLineProduct:
        payload = {
            "text": self._text,
            "speaker_wav": self._voice_model,
            "language": "en",
            "accent": "en",
        }

        # Call the TTS service
        response = requests.post(self._xtts_url, json=payload)

        if response and response.status_code == 200:
            # Convert and save the audio file
            return VoiceLineProduct(io.BytesIO(response.content), is_valid=True)
        else:
            return VoiceLineProduct(
                None,
                False,
                f"Failed with '{self._voice_model}'. HTTP Error: {response.status_code}",
            )

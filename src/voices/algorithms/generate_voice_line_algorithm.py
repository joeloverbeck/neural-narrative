from io import BytesIO

import numpy as np
import soundfile as sf

from src.voices.factories.voice_line_factory import VoiceLineFactory


class GenerateVoiceLineAlgorithm:
    def __init__(
        self,
        file_path: str,
        voice_line_factory: VoiceLineFactory,
    ):
        if not file_path:
            raise ValueError("file_path can't be empty.")

        self._file_path = file_path
        self._voice_line_factory = voice_line_factory

    @staticmethod
    def _convert_to_16bit(input_file: BytesIO, output_file=None):
        if output_file is None:
            output_file = input_file

        # Read the audio data from the file-like object
        data, samplerate = sf.read(input_file)

        # Process data as before
        if np.issubdtype(data.dtype, np.floating):
            data_16bit = np.int16(data * 32767)
        elif not np.issubdtype(data.dtype, np.int16):
            data_16bit = data.astype(np.int16)
        else:
            data_16bit = data

        # Write the 16-bit audio data back to a file
        sf.write(output_file, data_16bit, samplerate, subtype="PCM_16")

    def generate_voice_line(self) -> None:
        # Produce the voice line data
        product = self._voice_line_factory.create_voice_line()

        if not product.is_valid():
            raise ValueError(
                f"Failed to generate voice line. Error: {product.get_error()}"
            )

        # At this point, we have a juicy voice line in bytes format.
        self._convert_to_16bit(product.get(), self._file_path)

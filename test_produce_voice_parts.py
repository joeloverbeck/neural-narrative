from src.voices.factories.generate_voice_line_algorithm_factory import (
    GenerateVoiceLineAlgorithmFactory,
)
from src.voices.factories.produce_voice_parts_algorithm_factory import (
    ProduceVoicePartsAlgorithmFactory,
)
from src.voices.factories.voice_part_provider_factory import VoicePartProviderFactory


def main():
    character_name = "Gareth"

    voice_model = "npcmzeke"

    generate_voice_line_algorithm_factory = GenerateVoiceLineAlgorithmFactory()

    voice_part_provider_factory = VoicePartProviderFactory(
        character_name, voice_model, generate_voice_line_algorithm_factory
    )

    text_parts = [
        "*Gareth looks down.*",
        "Well, ain't that a funny thing.",
        "*Gareth's snorts.*",
        "My lower half is missin'.",
    ]

    timestamp = "test"

    produce_voice_parts_algorithm = ProduceVoicePartsAlgorithmFactory(
        voice_part_provider_factory
    ).create_algorithm(text_parts, timestamp)

    produce_voice_parts_algorithm.do_algorithm()


if __name__ == "__main__":
    main()

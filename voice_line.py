import random

from src.voices.factories.direct_voice_line_generation_algorithm_factory import (
    DirectVoiceLineGenerationAlgorithmFactory,
)


def generate_timestamp_between(start_timestamp, end_timestamp):
    start_time = int(start_timestamp[:14])
    end_time = int(end_timestamp[:14])
    random_time = random.randint(start_time, end_time)
    return f"{random_time}"


def generate_voice_line(
    previous_voice_line_name,
    following_voice_line_name,
    character_name,
    text,
    voice_model,
):
    determined_timestamp = generate_timestamp_between(
        previous_voice_line_name, following_voice_line_name
    )
    generated_voice_file = DirectVoiceLineGenerationAlgorithmFactory.create_algorithm(
        character_name, text, voice_model
    ).direct_voice_line_generation()
    print(
        f"Generated voice file '{generated_voice_file}' should have timestamp {determined_timestamp}."
    )


def main():
    print(
        "The purpose of this app is to generate a voice line that was missing from a dialogue."
    )
    print(
        "It will generate a voice line with a timestamp between the indicated voice line names."
    )
    generate_voice_line(
        "20241025140017-Elias Blackwood-molagbal",
        "20241025140059-Gideon Harrow-dbspectrallachance.wav",
        "Kael",
        "The Echoflora has its secrets, just like us. The initiation chamber... it's designed to test your inner strength, your resolve. What you experienced there, the visions, the sensations - they're a reflection of your own mind. The stronger your will, the more you'll gain from the experience. But remember, not everything is as it seems. The sanctuary's teachings are a double-edged sword; they can empower you or consume you, depending on how you wield them.",
        "npcfmarleneglass",
    )


if __name__ == "__main__":
    main()

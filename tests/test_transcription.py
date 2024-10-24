from src.dialogues.transcription import Transcription


def test_transcription_insufficient():
    # Setup
    transcription = Transcription()
    # Not adding any speech turns
    assert not transcription.is_transcription_sufficient()

    # Adding fewer than 5 speech turns
    for i in range(4):
        transcription.add_speech_turn("Speaker", f"Message {i}")
    assert not transcription.is_transcription_sufficient()

    # Adding 5 speech turns
    transcription.add_speech_turn("Speaker", "Message 4")
    assert transcription.is_transcription_sufficient()

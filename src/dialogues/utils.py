from typing import Optional


def format_speech(narration: Optional[str], speech: str) -> str:
    if narration and narration.strip().lower() != "none":
        speech_message = f"*{narration}* {speech}"
    else:
        speech_message = f"{speech}"

    return speech_message

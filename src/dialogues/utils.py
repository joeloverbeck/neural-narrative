from typing import Optional


def format_speech(narration: Optional[str], speech: str) -> str:
    if narration and narration.strip().lower() != "none":
        return f"*{narration}* {speech}"
    else:
        return f"{speech}"

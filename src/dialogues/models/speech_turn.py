from typing import Type, Optional

from pydantic import BaseModel, Field


def get_custom_speech_turn_class(speaker_name: str) -> Type[BaseModel]:
    class SpeechTurn(BaseModel):
        name: str = Field(
            ...,
            description=f"The name of the character who is speaking. In this case, {speaker_name}. Write ONLY as {speaker_name}, based on the bio above.",
        )
        narration_text: Optional[str] = Field(
            description=f"Narration text from an objective third person viewpoint, describing the character reactions and/or actions during {speaker_name}'s speech. Don't include {speaker_name}'s internal thoughts. Refer to the character by name. The narration text is optional, so only generate narration text if it truly adds value to {speaker_name}'s speech turn. Here is an example: {speaker_name} sits up and faces the interlocutor. Avoid repeating previous narration text belonging to {speaker_name}.",
            default=None,
        )
        speech: str = Field(
            ...,
            description=f"{speaker_name}'s generated speech that continues the provided dialogue. Pay attention to {speaker_name}'s speech patterns to determine the character's unique voice. Produce original speech. Try to vary the structure of the speech so that it contrasts with the character's previous utterances, and doesn't sound repetitive.",
        )
        thoughts: str = Field(
            ...,
            description=f"{speaker_name}'s thoughts related to this part of the dialogue. Adapt recent thoughts to the most recent part of the dialogue.",
        )
        desired_action: str = Field(
            ...,
            description=f"The action that {speaker_name} would like to take now, based on last stretch of the ongoing conversation. Adapt recent desired actions to the most recent part of the dialogue.",
        )

    return SpeechTurn

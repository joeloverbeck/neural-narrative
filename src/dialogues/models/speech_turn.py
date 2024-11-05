from typing import Type, Optional

from pydantic import BaseModel, Field


class Speech(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to generate the character's speech. It should be original material, relevant to the dialogue, "
        "and uniquely fitting to the character. Try to vary the structure of the speech so that it contrasts with the character's previous utterances, and doesn't sound repetitive. "
        "Important: avoid repeating previous lines of dialogue.",
    )
    speech: str


def get_custom_speech_turn_class(speaker_name: str) -> Type[BaseModel]:
    class SpeechTurn(BaseModel):
        name: str = Field(
            ...,
            description=(
                f"The name of the character who is speaking. In this case, {speaker_name}. Write ONLY as {speaker_name}, based on the bio above."
            ),
        )
        narration_text: Optional[str] = Field(
            description=f"Narration text in third person, describing the character's thoughts and/or actions during {speaker_name}'s speech. Refer to the character by their name. The narration text is optional, so only generate narration text if it truly adds value to {speaker_name}'s speech turn. Here is an example: {speaker_name} sits up and faces the interlocutor. Avoid repeating previous narration text belonging to {speaker_name}.",
            default=None,
        )
        speech: Speech = Field(
            ...,
            description=(
                f"{speaker_name}'s generated speech. Pay attention to {speaker_name}'s speech patterns to determine the character's unique voice. Important: do not repeat {speaker_name}'s previous utterances in the dialogue, and don't reword them either. Produce unique speech."
            ),
        )

    return SpeechTurn

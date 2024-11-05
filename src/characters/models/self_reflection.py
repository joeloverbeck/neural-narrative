from pydantic import BaseModel, Field

class Reflection(BaseModel):
    chain_of_thought: str = Field(
        ...,
        description="Think step by step to generate the character's self-reflection. "
    "The reflection should be meaningful and compelling, exploring the character's thoughts, feelings, and insights about their experiences.",
    )
    reflection: str


class SelfReflection(BaseModel):
    self_reflection: Reflection = Field(
        ...,
        description=(
            "The meaningful and compelling self-reflection in the third-person perspective of the character. Follow the provided instructions."
        ),
    )

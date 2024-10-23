from pydantic import BaseModel, Field, conlist


class Goals(BaseModel):
    goals: conlist(str, min_length=3, max_length=3) = Field(
        ...,
        description=(
            "A list of three intriguing and engaging short-term goals for the player to pursue. "
            "Follow the provided instructions."
        ),
    )

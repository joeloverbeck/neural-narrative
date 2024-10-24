from pydantic import BaseModel, Field


class TravelNarration(BaseModel):
    travel_narration: str = Field(
        ...,
        description=(
            "The narration of the act of traveling from the area of origin to the destination area. "
            "The narration must be written in the player's first-person perspective, based on their personality, "
            "profile, and memories. If the player is traveling with followers, you should try to incorporate them "
            "in the narration according to their personalities, profiles, and memories."
        ),
    )

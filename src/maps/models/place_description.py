from pydantic import BaseModel, Field


class PlaceDescription(BaseModel):
    description: str = Field(
        ...,
        description=(
            "The description of the place indicated above, filtered through the player's first-person perspective, "
            "as indicated in the instructions."
        ),
    )

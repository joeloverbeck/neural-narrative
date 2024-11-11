from pydantic import BaseModel, Field


class Foreshadowing(BaseModel):
    foreshadowing: str = Field(
        ...,
        description=(
            "An element that could serve as foreshadowing for future plot development. Follow the provided instructions."
        ),
    )

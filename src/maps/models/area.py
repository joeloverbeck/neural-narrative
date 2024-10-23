from pydantic import BaseModel, Field


class Area(BaseModel):
    name: str = Field(..., description="The name of the generated area.")
    description: str = Field(
        ...,
        description=(
            "The description of the generated area. Follow the instructions provided to produce this description."
        ),
    )

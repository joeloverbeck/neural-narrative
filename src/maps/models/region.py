from pydantic import BaseModel, Field


class Region(BaseModel):
    name: str = Field(..., description="The name of the generated region.")
    description: str = Field(
        ...,
        description=(
            "The description of the generated region. Follow the instructions provided to produce this description."
        ),
    )

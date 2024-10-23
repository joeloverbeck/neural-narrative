from pydantic import BaseModel, Field


class World(BaseModel):
    name: str = Field(..., description="The name of the generated world.")
    description: str = Field(
        ...,
        description=(
            "The description of the generated world. Follow the instructions provided to produce this description."
        ),
    )

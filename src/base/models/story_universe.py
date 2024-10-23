from pydantic import BaseModel, Field, conlist


class StoryUniverse(BaseModel):
    name: str = Field(..., description="The name of the generated story universe.")
    description: str = Field(
        ...,
        description=(
            "The description of the generated story universe. "
            "Follow the instructions provided to produce this description."
        ),
    )
    categories: conlist(str, min_length=2, max_length=2) = Field(
        ...,
        description=(
            "A list of two fitting categories for this story universe "
            "(such as high fantasy, dark fantasy, cyberpunk, horror, etc.)."
        ),
    )

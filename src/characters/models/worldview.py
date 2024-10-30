from pydantic import BaseModel, Field


class Worldview(BaseModel):
    worldview: str = Field(
        ...,
        description=(
            "The character's worldview, including their philosophical beliefs and moral standings. Follow the provided instructions."
        ),
    )

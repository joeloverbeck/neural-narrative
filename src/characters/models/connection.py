from pydantic import BaseModel, Field


class Connection(BaseModel):
    connection: str = Field(
        ...,
        description=(
            "The meaningful and compelling connection between two characters. Follow the provided instructions."
        ),
    )

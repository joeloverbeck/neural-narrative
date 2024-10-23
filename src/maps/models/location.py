from enum import Enum

from pydantic import BaseModel, Field

from src.base.constants import LOCATION_TYPES

# Dynamically create the Enum for Location types
LocationTypeEnum = Enum(
    "LocationTypeEnum",
    {name.replace(" ", "_"): name for name in LOCATION_TYPES},
)


class Location(BaseModel):
    name: str = Field(..., description="The name of the generated location.")
    description: str = Field(
        ...,
        description=(
            "The description of the generated location. "
            "Follow the instructions provided to produce this description."
        ),
    )
    type: LocationTypeEnum = Field(..., description="The type of location.")

    class Config:
        use_enum_values = True  # This ensures enums are serialized by their values

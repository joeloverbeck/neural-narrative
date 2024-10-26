from enum import Enum
from pathlib import Path
from typing import Type

from pydantic import BaseModel, Field

from src.filesystem.file_operations import read_file_lines, read_json_file


def get_custom_location_class() -> Type[BaseModel]:
    location_types = read_json_file(Path("data\paths\paths.json"))

    # Dynamically create the Enum for Location types
    location_type_enum = Enum(
        "LocationTypeEnum",
        {
            name.replace(" ", "_"): name
            for name in read_file_lines(Path(location_types["location_types"]))
        },
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
        type: location_type_enum = Field(..., description="The type of location.")

        class Config:
            use_enum_values = True  # This ensures enums are serialized by their values

    return Location

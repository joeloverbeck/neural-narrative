from enum import Enum
from typing import Type

from pydantic import BaseModel, Field

from src.filesystem.file_operations import read_file_lines
from src.filesystem.path_manager import PathManager


def get_custom_location_class() -> Type[BaseModel]:
    location_types = read_file_lines(PathManager.get_location_types_path())

    # Dynamically create the Enum for Location types
    location_type_enum = Enum(
        "LocationTypeEnum",
        {name.replace(" ", "_"): name for name in location_types},
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

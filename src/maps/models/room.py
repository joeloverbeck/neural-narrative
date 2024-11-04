from enum import Enum
from typing import Type

from pydantic import BaseModel, Field

from src.filesystem.file_operations import read_file_lines
from src.filesystem.path_manager import PathManager


def get_custom_room_class() -> Type[BaseModel]:
    room_types = read_file_lines(PathManager.get_room_types_path())

    # Dynamically create the Enum for Room types
    room_type_enum = Enum(
        "RoomTypeEnum",
        {name.replace(" ", "_"): name for name in room_types},
    )

    class Room(BaseModel):
        name: str = Field(..., description="The name of the generated room.")
        description: str = Field(
            ...,
            description=(
                "The description of the generated room. "
                "Follow the instructions provided to produce this description."
            ),
        )
        type: room_type_enum = Field(..., description="The type of room.")

        class Config:
            use_enum_values = True  # This ensures enums are serialized by their values

    return Room

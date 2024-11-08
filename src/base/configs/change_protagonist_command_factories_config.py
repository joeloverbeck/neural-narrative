from dataclasses import dataclass

from src.base.factories.remove_followers_command_factory import (
    RemoveFollowersCommandFactory,
)
from src.maps.factories.get_place_identifier_of_character_location_algorithm_factory import (
    GetPlaceIdentifierOfCharacterLocationAlgorithmFactory,
)
from src.maps.factories.remove_character_from_place_command_factory import (
    RemoveCharacterFromPlaceCommandFactory,
)
from src.movements.factories.place_character_at_place_command_factory import (
    PlaceCharacterAtPlaceCommandFactory,
)


@dataclass
class ChangeProtagonistCommandFactoriesConfig:
    place_character_at_place_command_factory: PlaceCharacterAtPlaceCommandFactory
    remove_followers_command_factory: RemoveFollowersCommandFactory
    get_place_identifier_of_character_location_algorithm_factory: (
        GetPlaceIdentifierOfCharacterLocationAlgorithmFactory
    )
    remove_character_from_place_command_factory: RemoveCharacterFromPlaceCommandFactory

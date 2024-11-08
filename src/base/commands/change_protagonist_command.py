from typing import Optional

from src.base.abstracts.command import Command
from src.base.configs.change_protagonist_command_config import (
    ChangeProtagonistCommandConfig,
)
from src.base.configs.change_protagonist_command_factories_config import (
    ChangeProtagonistCommandFactoriesConfig,
)
from src.base.playthrough_manager import PlaythroughManager


class ChangeProtagonistCommand(Command):

    def __init__(
        self,
        config: ChangeProtagonistCommandConfig,
        factories_config: ChangeProtagonistCommandFactoriesConfig,
        playthrough_manager: Optional[PlaythroughManager] = None,
    ):
        self._config = config
        self._factories_config = factories_config

        self._playthrough_manager = playthrough_manager or PlaythroughManager(
            self._config.playthrough_name
        )

    def execute(self) -> None:
        current_protagonist_identifier = (
            self._playthrough_manager.get_player_identifier()
        )
        current_place_identifier = (
            self._playthrough_manager.get_current_place_identifier()
        )

        # Place the current protagonist at the current place
        self._factories_config.place_character_at_place_command_factory.create_command(
            current_protagonist_identifier, current_place_identifier
        ).execute()

        # Get the current protagonist's followers
        followers = self._playthrough_manager.get_followers()

        # Remove followers and place them at the current place
        self._factories_config.remove_followers_command_factory.create_command(
            followers
        ).execute()

        # Update the player identifier to the new protagonist
        self._playthrough_manager.update_player_identifier(
            self._config.new_protagonist_identifier
        )

        # Finally, we need to update the current place of the playthrough, which should be the place where
        # the new protagonist identifier was.
        place_identifier = self._factories_config.get_place_identifier_of_character_location_algorithm_factory.create_algorithm(
            self._config.new_protagonist_identifier
        ).do_algorithm()

        # We now know where the character who's the new protagonist was before.
        self._factories_config.remove_character_from_place_command_factory.create_command(
            self._config.new_protagonist_identifier, place_identifier
        ).execute()

        # Change the current place to the place_identifier.
        self._playthrough_manager.update_current_place(place_identifier)

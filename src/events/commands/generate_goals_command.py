import logging
from typing import cast, Optional

from src.abstracts.command import Command
from src.events.factories.goals_factory import GoalsFactory
from src.events.products.goals_product import GoalsProduct
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GenerateGoalsCommand(Command):
    def __init__(
        self,
        playthrough_name: str,
        goals_factory: GoalsFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        self._playthrough_name = playthrough_name
        self._goals_factory = goals_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def execute(self) -> None:

        product = cast(GoalsProduct, self._goals_factory.generate_product())

        if not product.is_valid():
            raise ValueError(
                f"Was unable to generate goals. Error: {product.get_error()}"
            )

        generated_goals = product.get()

        goals = ""

        for goal in generated_goals:
            if goal:
                goals += "\n" + goal

        # At this point, we have our goals, so we save them.
        self._filesystem_manager.append_to_file(
            self._filesystem_manager.get_file_path_to_goals(self._playthrough_name),
            goals,
        )

        logger.info("Saved goals.")

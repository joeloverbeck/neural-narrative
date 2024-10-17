import logging
from typing import Optional, List

from src.concepts.factories.plot_blueprints_factory import PlotBlueprintsFactory
from src.exceptions import PlotBlueprintGenerationError
from src.filesystem.filesystem_manager import FilesystemManager

logger = logging.getLogger(__name__)


class GeneratePlotBlueprintsAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        plot_blueprints_factory: PlotBlueprintsFactory,
        filesystem_manager: Optional[FilesystemManager] = None,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._playthrough_name = playthrough_name
        self._plot_blueprints_factory = plot_blueprints_factory

        self._filesystem_manager = filesystem_manager or FilesystemManager()

    def do_algorithm(self) -> List[str]:
        product = self._plot_blueprints_factory.generate_product()

        if not product.is_valid():
            error_message = (
                f"Failed to generate plot blueprints. Error: {product.get_error()}",
            )
            logger.error(error_message)

            raise PlotBlueprintGenerationError(error_message)

        prettified_plot_blueprints = ""

        for plot_blueprint in product.get():
            prettified_plot_blueprints += "\n" + str(plot_blueprint).replace(
                "\n\n", " "
            )

        # Got the plot blueprints, now have to save them.
        self._filesystem_manager.append_to_file(
            self._filesystem_manager.get_file_path_to_plot_blueprints(
                self._playthrough_name
            ),
            prettified_plot_blueprints,
        )

        logger.info("Saved plot blueprints.")

        return product.get()

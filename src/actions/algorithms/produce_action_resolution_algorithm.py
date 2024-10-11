from typing import cast

from src.actions.algorithms.produce_voice_lines_for_action_resolution_algorithm import (
    ProduceVoiceLinesForActionResolutionAlgorithm,
)
from src.actions.algorithms.store_action_resolution_algorithm import (
    StoreActionResolutionAlgorithm,
)
from src.actions.products.action_resolution_product import ActionResolutionProduct
from src.prompting.providers.base_tool_response_provider import BaseToolResponseProvider


class ProduceActionResolutionAlgorithm:
    def __init__(
        self,
        playthrough_name: str,
        action_resolution_factory: BaseToolResponseProvider,
        store_action_resolution_algorithm: StoreActionResolutionAlgorithm,
        produce_voice_lines_for_action_resolution_algorithm: ProduceVoiceLinesForActionResolutionAlgorithm,
    ):
        if not playthrough_name:
            raise ValueError("playthrough_name can't be empty.")

        self._action_resolution_factory = action_resolution_factory
        self._store_action_resolution_algorithm = store_action_resolution_algorithm
        self._produce_voice_lines_for_action_resolution_algorithm = (
            produce_voice_lines_for_action_resolution_algorithm
        )

    def do_algorithm(self) -> ActionResolutionProduct:
        product = cast(
            ActionResolutionProduct,
            self._action_resolution_factory.generate_product(),
        )

        if not product.is_valid():
            raise ValueError(
                f"The generation of an action resolution failed. Error: {product.get_error()}"
            )

        self._store_action_resolution_algorithm.do_algorithm(product)

        self._produce_voice_lines_for_action_resolution_algorithm.do_algorithm(product)

        return product

from src.concepts.algorithms.base_concept_algorithm import BaseConceptAlgorithm
from src.concepts.factories.scenarios_factory import (
    ScenariosFactory,
)
from src.concepts.products.scenarios_product import (
    ScenariosProduct,
)


class GenerateScenariosAlgorithm(
    BaseConceptAlgorithm[ScenariosProduct, ScenariosFactory]
):
    pass

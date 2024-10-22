from src.maps.abstracts.factory_products import CardinalConnectionCreationProduct


class ConcreteCardinalConnectionCreationProduct(
    CardinalConnectionCreationProduct):

    def __init__(self, was_successful: bool, error: str = None):
        self._was_successful = was_successful
        self._error = error

    def was_successful(self) -> bool:
        return self._was_successful

    def get_error(self) -> str:
        return self._error

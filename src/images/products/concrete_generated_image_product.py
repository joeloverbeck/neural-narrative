from src.images.abstracts.factory_products import GeneratedImageProduct


class ConcreteGeneratedImageProduct(GeneratedImageProduct):
    def __init__(self, image_url: str, is_valid: bool, error: str = None):
        self._image_url = image_url
        self._is_valid = is_valid
        self._error = error

    def get(self) -> str:
        return self._image_url

    def is_valid(self) -> bool:
        return self._is_valid

    def get_error(self) -> str:
        return self._error

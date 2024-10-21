from typing import Protocol

from src.base.required_string import RequiredString
from src.images.abstracts.factory_products import GeneratedImageProduct


class GeneratedImageFactory(Protocol):
    def generate_image(self, prompt: RequiredString) -> GeneratedImageProduct:
        pass

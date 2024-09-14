from typing import Protocol

from src.images.abstracts.factory_products import GeneratedImageProduct


class GeneratedImageFactory(Protocol):
    def generate_image(self, prompt: str) -> GeneratedImageProduct:
        pass

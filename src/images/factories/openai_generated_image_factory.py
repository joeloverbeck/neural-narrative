from openai import BadRequestError
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.images.abstracts.factory_products import GeneratedImageProduct
from src.images.products.concrete_generated_image_product import ConcreteGeneratedImageProduct
from src.prompting.abstracts.llm_client import LlmClient


class OpenAIGeneratedImageFactory(GeneratedImageFactory):

    def __init__(self, llm_client: LlmClient):
        if not llm_client:
            raise ValueError("llm_client can't be empty.")
        self._llm_client = llm_client

    def generate_image(self, prompt: str) -> GeneratedImageProduct:
        try:
            return ConcreteGeneratedImageProduct(self._llm_client.
                                                 generate_image(prompt), is_valid=True)
        except BadRequestError as error:
            return ConcreteGeneratedImageProduct(None, is_valid=False,
                                                 error=f'Was unable to generate image: {error}')

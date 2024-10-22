from dataclasses import dataclass
from src.characters.factories.character_description_provider_factory import CharacterDescriptionProviderFactory
from src.characters.factories.character_factory import CharacterFactory
from src.images.abstracts.abstract_factories import GeneratedImageFactory
from src.requests.abstracts.abstract_factories import UrlContentFactory


@dataclass
class GenerateCharacterImageCommandFactoriesConfig:
    character_factory: CharacterFactory
    character_description_provider_factory: CharacterDescriptionProviderFactory
    generated_image_factory: GeneratedImageFactory
    url_content_factory: UrlContentFactory

from dataclasses import dataclass


@dataclass
class SecretsFactoryConfig:
    character_identifier: str
    query_text: str

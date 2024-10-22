from typing import List


class StoryUniverseProduct:

    def __init__(self, name: str, description: str, categories: List[str]):
        self._name = name
        self._description = description
        self._categories = categories

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_categories(self) -> List[str]:
        return self._categories

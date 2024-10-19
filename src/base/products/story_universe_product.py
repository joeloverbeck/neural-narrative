from typing import List

from src.base.playthrough_name import RequiredString


class StoryUniverseProduct:

    def __init__(
        self,
        name: RequiredString,
        description: RequiredString,
        categories: List[RequiredString],
    ):
        self._name = name
        self._description = description
        self._categories = categories

    def get_name(self) -> RequiredString:
        return self._name

    def get_description(self) -> RequiredString:
        return self._description

    def get_categories(self) -> List[RequiredString]:
        return self._categories

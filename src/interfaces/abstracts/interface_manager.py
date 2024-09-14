from typing import Protocol, Optional, List


class InterfaceManager(Protocol):
    def prompt_for_character_identifier(self, prompt_text: str) -> Optional[str]:
        pass

    @staticmethod
    def prompt_for_multiple_identifiers(prompt_text: str) -> List[str]:
        pass

    @staticmethod
    def prompt_for_input(prompt_text: str) -> str:
        pass

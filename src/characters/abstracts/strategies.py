from typing import Protocol, List


class OtherCharactersIdentifiersStrategy(Protocol):
    def get_data(self) -> List[str]:
        pass

from abc import ABC, abstractmethod


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, message: dict) -> None:
        """
        Receive update from subject.
        """
        pass

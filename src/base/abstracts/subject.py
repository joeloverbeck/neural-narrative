from __future__ import annotations

from typing import Protocol

from src.base.abstracts.observer import Observer


class Subject(Protocol):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    def notify(self, message: dict) -> None:
        """
        Notify all observers about an event.
        """
        pass

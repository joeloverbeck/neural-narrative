from abc import abstractmethod, ABC


class PlaceGenerationStrategy(ABC):
    @abstractmethod
    def generate_place(self):
        pass

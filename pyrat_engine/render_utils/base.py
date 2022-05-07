from abc import ABC, abstractmethod

from pyrat_engine.state.base import CurrentGameState


class Render(ABC):
    @abstractmethod
    def initialize(self):
        """Initialize the resource for displaying"""
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def render(self, state: CurrentGameState) -> None:
        """Processes the CurrentGameState and prints it"""
        pass

    @abstractmethod
    def __enter__(self):
        """Allows this printer to be used as a context manager"""
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager"""
        pass

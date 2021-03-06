from abc import ABC, abstractmethod
from typing import Any

from pyrat_engine.state.base import CurrentGameState


class Renderer(ABC):
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the resource for displaying"""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the resources acquired for displaying"""
        pass

    @abstractmethod
    def render(self, state: CurrentGameState) -> Any:
        """Processes the CurrentGameState and prints it"""
        pass

    def __enter__(self) -> Any:
        """Allows this printer to be used as a context manager"""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Any:
        """Exit the context manager"""
        self.close()

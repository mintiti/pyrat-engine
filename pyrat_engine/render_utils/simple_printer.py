from typing import Any

from pyrat_engine.render_utils.base import Renderer
from pyrat_engine.state.base import CurrentGameState


class SimplePrinter(Renderer):
    def initialize(self) -> None:
        """Simple Printer doesn't acquire anything"""
        pass

    def close(self) -> None:
        """Simple Printer doesn't acquire anything"""
        pass

    def render(self, state: CurrentGameState) -> None:
        def grid(width, height):
            sep = "\n" + "+---" * width + "+\n"
            return sep + ("|   " * width + "|" + sep) * height

        print(grid(state.maze_width, state.maze_height))

    def __enter__(self) -> "SimplePrinter":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> Any:
        pass

    def __init__(self):
        pass

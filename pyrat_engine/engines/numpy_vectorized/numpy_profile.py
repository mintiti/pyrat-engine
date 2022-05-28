"""Convenience file to define functions to use for the profiler"""
import random

from pyrat_engine.benchmarking.config import BenchmarkConfig
from pyrat_engine.engines.numpy_vectorized.engine import NumpyEngine
from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.types import Move

if __name__ == "__main__":
    nb_moves_per_run = 200
    state_initializer = CurrentStateInitializer()
    benchmark_config = BenchmarkConfig(nb_moves_per_run=nb_moves_per_run)
    state = state_initializer()
    engine = NumpyEngine(state)
    list_moves = list(Move)
    for _ in range(nb_moves_per_run):
        p1_move: Move = random.choice(list_moves)
        p2_move: Move = random.choice(list_moves)
        engine.move(p1_move, p2_move)

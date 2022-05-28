"""Convenience file to define functions to use for the profiler"""

from pyrat_engine.benchmarking.profile_utils import profile_move
from pyrat_engine.engines.numpy_vectorized.engine import NumpyEngine

if __name__ == "__main__":
    profile_move(NumpyEngine, 200)

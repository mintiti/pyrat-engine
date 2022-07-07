"""Convenience file to define functions to use for the profiler"""

from pyrat_engine.benchmarking.profile_utils import profile_move
from pyrat_engine.engines.vanilla_py.vanilla_py_engine import VanillaPyEngine

if __name__ == "__main__":
    profile_move(VanillaPyEngine, 2000)

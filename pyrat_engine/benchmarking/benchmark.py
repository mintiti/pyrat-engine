from typing import Callable, List

import gc
import random
from timeit import Timer

from pyrat_engine.benchmarking.config import BenchmarkConfig
from pyrat_engine.engines.base import PyratEngine
from pyrat_engine.initializer.initializer import CurrentStateInitializer
from pyrat_engine.state.base import CurrentGameState
from pyrat_engine.types import Move


def run_moves(engine: PyratEngine, state: CurrentGameState, nb_moves: int) -> float:
    """Run a series of nb_moves on the given state using the provided engine"""

    def setup():
        engine.set_current_game_state(state)
        gc.enable()

    def run():
        for _ in range(nb_moves):
            p1_move: Move = random.choice(list(Move))
            p2_move: Move = random.choice(list(Move))
            engine.move(p1_move, p2_move)

    timer = Timer(stmt=run, setup=setup)
    return timer.timeit(number=1)


def run_benchmark(
    engine_cls: Callable[..., PyratEngine], bench_config: BenchmarkConfig
) -> List[float]:
    """Run the full benchmark"""
    state_initializer = CurrentStateInitializer(
        player_config=bench_config.player_config, maze_config=bench_config.maze_config
    )
    times = []
    for _ in range(bench_config.nb_runs):
        # Run 1 run and get the times

        # Create the state
        state = state_initializer()
        engine = engine_cls(state)
        run_times = run_moves(engine, state, bench_config.nb_moves_per_run)
        times.append(run_times)

    return times

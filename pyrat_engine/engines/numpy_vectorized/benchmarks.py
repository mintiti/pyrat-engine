from pyrat_engine.benchmarking.benchmark import run_benchmark
from pyrat_engine.benchmarking.config import BenchmarkConfig
from pyrat_engine.engines.numpy_vectorized import NumpyEngine

if __name__ == "__main__":
    times = run_benchmark(NumpyEngine, BenchmarkConfig())
    print(f"mean time for a move operation : {sum(times)/len(times)}")

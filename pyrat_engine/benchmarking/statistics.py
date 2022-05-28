from typing import Dict, List


def get_statistics(times: List[float]) -> Dict[str, float]:
    assert len(times) != 0, "Times list is empty, please provide a non empty list"
    mean = sum(times) / len(times)
    statistics = {"mean": mean}
    return statistics

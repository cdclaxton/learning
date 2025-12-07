import os
from datetime import datetime


def silly_op(context: str, value: float = 2.0, n_ops: int = 10000):
    """Expensive, CPU-bound operation."""

    print(f"[pid={os.getpid()}] [{context}] {datetime.now()} Processing value: {value}")
    for _ in range(n_ops):
        value *= 2
        value /= 2
    return {"value": value, "pid": os.getpid()}

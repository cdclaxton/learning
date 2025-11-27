import asyncio
import multiprocessing
import time

from typing import List, Tuple


def silly_operation(value: float, n_ops: int) -> float:
    for i in range(n_ops):
        value *= 2
        value /= 2
    return value


async def async_silly_operation(value: float, n_ops: int) -> float:
    for i in range(n_ops):
        value *= 2
        value /= 2
    return value


async def main(ops):
    asyncio.gather(*(async_silly_operation(value, n_ops) for value, n_ops in ops))


def main_multiprocess(ops: List[Tuple[int, int]]):
    """
    Uses a multiprocessing Pool to execute the silly_operation
    function in parallel across multiple CPU cores.
    """
    # Determine the number of processes to use (usually one per core)
    num_processes = multiprocessing.cpu_count()

    # Create a pool of worker processes
    print(f"Starting multiprocessing Pool with {num_processes} processes...")
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(silly_operation, ops)

    # The pool context manager automatically handles closing and joining the processes
    return results


if __name__ == "__main__":

    ops = [(10, 10000000), (20, 10000000), (30, 10000000)]

    # Sequential computation
    start = time.perf_counter()
    for value, n_ops in ops:
        result = silly_operation(value, n_ops)
        assert value == result
    stop = time.perf_counter()
    print(f"Sequentially: Time taken = {stop - start} seconds")

    # Using async
    start = time.perf_counter()
    asyncio.run(main(ops))
    stop = time.perf_counter()
    print(f"async: Time taken = {stop - start} seconds")

    # Using multiprocessing
    start = time.perf_counter()
    main_multiprocess(ops)
    stop = time.perf_counter()
    print(f"multiprocessing: Time taken = {stop - start} seconds")

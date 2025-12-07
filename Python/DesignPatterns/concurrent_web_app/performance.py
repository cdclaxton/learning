import aiohttp
import asyncio
import numpy as np
import pandas as pd
import requests
import time

from silly_operation import silly_op

URL = "http://localhost:8000"


def make_url(endpoint: str, value: float, n_ops: int):
    return URL + endpoint + f"?value={value}&n_ops={n_ops}"


async def perform_request(
    session: aiohttp.ClientSession, endpoint: str, value: float, n_ops: int
):

    # Send the GET request
    url = make_url(endpoint, value, n_ops)
    response = await session.get(url=url)

    # Check the response
    assert response.status == 200, f"Got status code: {response.status} from URL {url}"
    data = await response.json()
    assert data["value"] == value

    return data


async def time_requests(
    endpoint: str, n_simultaneous_requests: int, value: float, n_ops: int
):

    async with aiohttp.ClientSession() as client_session:
        tasks = []
        start_time = time.perf_counter()
        for _ in range(n_simultaneous_requests):
            tasks.append(perform_request(client_session, endpoint, value, n_ops))

        await asyncio.gather(*tasks, return_exceptions=False)

    return time.perf_counter() - start_time, tasks


async def experiment2(
    endpoint: str, n_simultaneous_requests: int, value: float, n_ops: int
):
    async with aiohttp.ClientSession() as client_session:
        tasks = []
        start_time = time.perf_counter()
        for _ in range(n_simultaneous_requests):
            tasks.append(perform_request(client_session, endpoint, value, n_ops))

        result = await asyncio.gather(*tasks, return_exceptions=False)

    return time.perf_counter() - start_time, result


if __name__ == "__main__":

    endpoints = ["/asyncio", "/sync", "/asyncio2"]
    value = 50.0
    n_ops = 100_000_000
    n_simultaneous_requests = 4
    n_runs = 1

    # Function time
    start_time = time.perf_counter()
    silly_op("Single function execution", value, n_ops)
    print(f"Function execution time: {time.perf_counter() - start_time} seconds")

    # Single call
    start_time = time.perf_counter()
    requests.get(make_url("/sync", value, n_ops))
    print(f"API call time: {time.perf_counter() - start_time} seconds")

    run_experiment1 = False
    run_experiment2 = True

    # -------------------------------------------------------------------------
    # Experiment 1
    # -------------------------------------------------------------------------

    if run_experiment1:
        for endpoint in endpoints:

            times = np.zeros(n_runs)
            for idx in range(n_runs):
                times[idx], _ = asyncio.run(
                    time_requests(endpoint, n_simultaneous_requests, value, n_ops)
                )

            print(
                f"Endpoint: {endpoint}, mean time taken for {n_simultaneous_requests} requests = {times.mean()} seconds (std dev = {times.std()})"
            )

    # -------------------------------------------------------------------------
    # Experiment 2
    # -------------------------------------------------------------------------

    if run_experiment2:
        n_experiment_2_runs = 100
        time_taken = np.zeros((n_experiment_2_runs))
        n_unique_pids = np.zeros((n_experiment_2_runs))

        for i in range(n_experiment_2_runs):
            print(f"Running experiment {i+1}/{n_experiment_2_runs}")
            time_taken[i], results = asyncio.run(
                experiment2("/sync", n_simultaneous_requests, value, n_ops)
            )

            n_unique_pids[i] = len(set([r["pid"] for r in results]))

        df = pd.DataFrame(
            {
                "time_taken": time_taken,
                "n_unique_pids": n_unique_pids,
            }
        )

        df.to_pickle("experiment_2_results.pkl")

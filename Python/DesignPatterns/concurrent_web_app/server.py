import asyncio
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager

from silly_operation import silly_op


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.executor = ProcessPoolExecutor()  # default: one worker per CPU core
    try:
        yield
    finally:
        app.state.executor.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return "Hello, World!"


@app.get("/asyncio")
async def asyncio_route(value: float = 2.0, n_ops: int = 10000):
    return silly_op("asyncio", value, n_ops)


@app.get("/sync")
def sync_route(value: float = 2.0, n_ops: int = 10000):
    return silly_op("sync", value, n_ops)


@app.get("/asyncio2")
async def sync_route2(value: float = 2.0, n_ops: int = 10000):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        app.state.executor, silly_op, "asyncio2", value, n_ops
    )

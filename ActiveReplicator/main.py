from manager.load_config import CONFIG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from psycopg2.pool import ThreadedConnectionPool
import colorama

import endpoints

colorama.init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.baseConnectionPool = ThreadedConnectionPool(
            1,
            8,
            user=CONFIG["DB_USER"],
            password=CONFIG["DB_PASSWORD"],
            host=CONFIG["DB_HOST"],
            port=CONFIG["DB_PORT"],
            database="auth"
        )
        print(colorama.Fore.RED + "SUCCESS: Established connection with base database")
    except Exception as e:
        app.state.baseConnectionPool = None
        print(colorama.Fore.RED + "ERROR: Failed to establish connection pool with base database, falling back on redundant database")

    try:
        app.state.redundantConnectionPool = ThreadedConnectionPool(
            1,
            8,
            user=CONFIG["DB_USER"],
            password=CONFIG["DB_PASSWORD"],
            host=CONFIG["DB_HOST"],
            port=CONFIG["DB_PORT"],
            database="auth"
        )
        print(colorama.Fore.RED + "SUCCESS: Established connection with redundant database")
    except Exception as e:
        app.state.redundantConnectionPool = None
        print(colorama.Fore.RED + "ERROR: Failed to establish connection pool with redundant database")

    yield

    if isinstance(app.state.baseConnectionPool, ThreadedConnectionPool):
        app.state.baseConnectionPool.closeall()
    if isinstance(app.state.redundantConnectionPool, ThreadedConnectionPool):
        app.state.redundantConnectionPool.closeall()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router)

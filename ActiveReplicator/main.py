from manager.load_config import CONFIG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from mysql.connector.pooling import MySQLConnectionPool
import colorama

import endpoints

colorama.init(autoreset=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.baseConnectionPool = MySQLConnectionPool(
            host=CONFIG["DB_HOST"],
            user=CONFIG["DB_USER"],
            password=CONFIG["DB_PASSWORD"],
            pool_name="base_pool",
            pool_size=8
        )
        print(colorama.Fore.GREEN + "SUCCESS: Established connection with base database")
    except Exception as e:
        app.state.baseConnectionPool = None
        print(colorama.Fore.RED + "ERROR: Failed to establish connection pool with base database, falling back on redundant database")
        print(e)

    try:
        app.state.redundantConnectionPool = MySQLConnectionPool(
            host=CONFIG["REDUNDANT_HOST"],
            user=CONFIG["REDUNDANT_USER"],
            password=CONFIG["REDUNDANT_PASSWORD"],
            pool_name="redundant_pool",
            pool_size=8
        )
        print(colorama.Fore.GREEN + "SUCCESS: Established connection with redundant database")
    except Exception as e:
        app.state.redundantConnectionPool = None
        print(colorama.Fore.RED + "ERROR: Failed to establish connection pool with redundant database")
        print(e)

    yield

    if app.state.baseConnectionPool is not None:
        app.state.baseConnectionPool._remove_connections()

    if app.state.redundantConnectionPool is not None:
        app.state.redundantConnectionPool._remove_connections()
        


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

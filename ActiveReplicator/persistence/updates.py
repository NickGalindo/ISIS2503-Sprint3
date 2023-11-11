from fastapi import HTTPException, status
from psycopg2.pool import ThreadedConnectionPool

from colorama import Fore

async def run(redundantPool: ThreadedConnectionPool, basePool: ThreadedConnectionPool, com: str):
    result = None

    try:
        assert(isinstance(basePool, ThreadedConnectionPool))

        db_connection = basePool.getconn()
        db_cursor = db_connection.cursor()

        db_cursor.execute(com)
        result = db_cursor.fetchall()

        db_cursor.close()
        
        basePool.putconn(db_connection)
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on base database, falling back to redundant database")

    try:
        assert(isinstance(redundantPool, ThreadedConnectionPool))

        db_connection = redundantPool.getconn()
        db_cursor = db_connection.cursor()

        db_cursor.execute(com)
        result = db_cursor.fetchall()

        db_cursor.close()

        redundantPool.putconn(db_connection)
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on redundant database, no connection open")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not establish any valid connection with database",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return result

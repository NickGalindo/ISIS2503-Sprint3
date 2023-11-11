from fastapi import HTTPException, status
from mysql.connector import connect

from colorama import Fore

async def query(redundantPool, basePool, com: str):
    result = None

    try:
        db_cursor = basePool.cursor()

        db_cursor.execute(com)
        result = db_cursor.fetchall()

        db_cursor.close()

        return result
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on base database, falling back to redundant database")
        print(e)


    try:
        db_cursor = redundantPool.cursor()

        db_cursor.execute(com)
        result = db_cursor.fetchall()

        db_cursor.close()

        return result
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on redundant database, no connection open")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not establish any valid connection with database",
            headers={"WWW-Authenticate": "Bearer"}
        )

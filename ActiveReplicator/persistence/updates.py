from fastapi import HTTPException, status
from mysql.connector import connect

from colorama import Fore

async def run(redundantPool, basePool, com: str):
    result = None

    try:
        db_cursor = basePool.cursor()

        db_cursor.execute(com)

        basePool.commit()

        db_cursor.close()

        print(result)
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on base database, falling back to redundant database")
        print(e)


    try:
        db_cursor = redundantPool.cursor()

        db_cursor.execute(com)

        redundantPool.commit()

        db_cursor.close()

        print(result)
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on redundant database, no connection open")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not establish any valid connection with database",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return "Success"

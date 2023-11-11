from fastapi import HTTPException, status
from mysql.connector.pooling import MySQLConnectionPool

from colorama import Fore

async def run(redundantPool: MySQLConnectionPool, basePool: MySQLConnectionPool, com: str):
    result = None

    try:
        assert(isinstance(basePool, MySQLConnectionPool))

        db_connection = basePool.get_connection()
        db_cursor = db_connection.cursor()

        db_cursor.execute(com)
        result = db_cursor.fetchall()

        #db_connection.commit()

        db_cursor.close()
        db_connection.close()

        print(result)
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on base database, falling back to redundant database")
        print(e)


    try:
        assert(isinstance(redundantPool, MySQLConnectionPool))

        db_connection = redundantPool.get_connection()
        db_cursor = db_connection.cursor()

        db_cursor.execute(com)
        result = db_cursor.fetchall()

        #db_connection.commit()

        db_cursor.close()
        db_connection.close()

        print(result)
    except Exception as e:
        print(Fore.RED + "ERROR: Failed to execute on redundant database, no connection open")
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not establish any valid connection with database",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return result

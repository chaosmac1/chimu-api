# Module Imports
import mariadb
import sys

from os import environ

dbPool: mariadb.ConnectionPool = None


def InitializeMySQL():
    print('MySQL: Initializing...')

    pool = None

    try:
        pool = mariadb.ConnectionPool(
            user=environ.get('MYSQL_USERNAME'),
            password=environ.get('MYSQL_PASSWORD'),
            host=environ.get('MYSQL_HOSTNAME'),
            database=environ.get('MYSQL_DATABASE'),
            port=3306,
            pool_name='chimu-api-v1',
            pool_size=16
        )

        print('MySQL: Test for connection')

        pool.get_connection().close()

        print('MySQL: Success')

    except mariadb.OperationalError as e:
        print(f'MySQL: Error opening an connection: {e}')
        print('Exiting...')
        exit(1)

    except mariadb.PoolError as e:
        print(f'MySQL: Error opening connection from pool: {e}')
        exit(1)

    global dbPool
    dbPool = pool


def GetDatabasePool():
    return dbPool


def GetDatabaseConnection():
    try:
        return GetDatabasePool().get_connection()
    except mariadb.PoolError as e:
        print("Failed to receive Pool!")
        print(e)
        return mariadb.connection(
            user=environ.get('MYSQL_USERNAME'),
            password=environ.get('MYSQL_PASSWORD'),
            host=environ.get('MYSQL_HOSTNAME'),
            database=environ.get('MYSQL_DATABASE'),
            port=3306,
            pool_name='chimu-api-v1',
            pool_size=16
        )

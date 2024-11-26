import psycopg2
from psycopg2 import extras
from psycopg2.extras import RealDictRow


class DB(object):
    def __init__(self, host, port, dbName, user, password):
        self.__connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbName,
            user=user,
            password=password,
        )
        self.__connection.autocommit = True

    def cursor(self, query) -> list[RealDictRow]:
        with self.__connection.cursor(cursor_factory=extras.RealDictCursor) as cursor:
            cursor.execute(query)
            try:
                result = cursor.fetchall()
                return result
            except psycopg2.ProgrammingError:
                return None
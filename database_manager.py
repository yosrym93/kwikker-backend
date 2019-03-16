import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseManager:
    def __init__(self):
        self.connection = None

    def initialize_connection(self, db_name, db_username, db_password):
        # Create the connection string
        connection_str: str = f"dbname='{db_name}' user='{db_username}' password='{db_password}'"
        # initialize connection to the database
        try:
            self.connection = psycopg2.connect(connection_str)
        except Exception as E:
            return E
        return None  # meaning everything was okay

    def execute_query_no_return(self, query: str, data=None):
        with self.connection.cursor() as cursor:
            try:
                if data is not None:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                self.connection.commit()
            except Exception as E:
                self.connection.rollback()
                return E
            return None  # meaning everything was okay

    def execute_query(self, query: str, data=None):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                if data is not None:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                self.connection.commit()
            except Exception as E:
                self.connection.rollback()
                return E
            return cursor.fetchall()


db_manager = DatabaseManager()

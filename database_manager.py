import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseManager:
    """
        Handles connection to the database such as:
        - Initializing connection.
        - Executing queries.
        - Accessing query results.
    """
    def __init__(self):
        self.connection = None

    def initialize_connection(self, db_name, db_username, db_password):
        """
            Initializes the connection to the database.


            *Parameters:*
                - *db_name*: The PostgreSQL database name.
                - *db_username*: The database username.
                - *db_password*: The database password.

            *Returns:*
                - *None*: If the database connection was successful.
                - *Exception* object: The exception thrown by the database connector if the connection failed.

        """
        # Create the connection string
        connection_str: str = f"dbname='{db_name}' user='{db_username}' password='{db_password}'"
        # initialize connection to the database
        try:
            self.connection = psycopg2.connect(connection_str)
        except Exception as E:
            return E
        return None  # meaning everything was okay

    def execute_query_no_return(self, query: str, data=None):
        """
            Executes a query that has no table results, such as inserts, updates and deletes.
            Inserting parameters into queries should not be done through string concatenation.
            Any parameters in the query are replaced with `'%s'` and a second argument is provided that
            contains the query parameters.
            For more information please refer to `pyscopg2 documentation <http://initd.org/psycopg/docs/usage.html>`_


            *Parameters:*
                - *query*: The SQL query.
                - *data*: Optional. The parameters of the query. Default: *None*

            *Returns:*
                - *None*: If the query was executed successfully.
                - *Exception* object: If the query produced an error.

        """
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
        """
            Executes a query that has table results, such as select queries.
            Inserting parameters into queries should not be done through string concatenation.
            Any parameters in the query are replaced with `'%s'` and a second argument is provided that
            contains the query parameters.
            For more information please refer to `pyscopg2 documentation <http://initd.org/psycopg/docs/usage.html>`_


            *Parameters:*
                - *query*: The SQL query.
                - *data*: Optional. The parameters of the query. Default: *None*

            *Returns:*
                - | *List of Dictionaries*: If the query was executed successfully.
                  | Each list element is a dictionary corresponding to a row in the query results.
                  | The dictionary keys are the column names of the query results.
                  | An empty list is returned if the query was successful but the result was an empty table.
                - *Exception* object: If the query produced an error.

        """
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
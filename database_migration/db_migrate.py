import psycopg2
import os
import datetime
import sys

sys.path.append('..')
import database_manager, app

db_manager = database_manager.db_manager
app = app.app

db_username = app.config['DATABASE_USERNAME']
db_password = app.config['DATABASE_PASSWORD']
db_name = app.config['DATABASE_NAME']
migrations_db_name = app.config['MIGRATIONS_DATABASE_NAME']


def check_migrations_db():
    # Check if the migrations database exist
    response = db_manager.initialize_connection(db_name=migrations_db_name,
                                                db_username=db_username, db_password=db_password)
    if isinstance(response, psycopg2.OperationalError):
        # Migrations database does not exist, connect to the default database
        print('Migration database does not exist..')
        print('Connecting to the default (postgres) database..')
        response = db_manager.initialize_connection(db_name='postgres', db_username=db_username,
                                                    db_password=db_password)
        if response is not None:
            print('Could not connect to postgres database!')
            print(response)
            return False

        print('Connected.')
        print('Creating migrations database..')
        db_manager.connection.autocommit = True
        response = db_manager.execute_query_no_return('CREATE DATABASE MIGRATIONS')
        db_manager.connection.autocommit = False

        if response is not None:
            print('Migrations database could not be created!')
            print(response)
            return False

        print('Migrations database created successfully, connecting to migrations database..')
        db_manager.close_connection()
        response = db_manager.initialize_connection(db_name=migrations_db_name,
                                                    db_username=db_username, db_password=db_password)
        if response is not None:
            print('Could not connect to migrations database!')
            print(response)
            return False

        print('Connected. Creating tables..')
        response = db_manager.execute_query_no_return("""
                                                        CREATE TABLE MIGRATION(
                                                            FILE_NAME   VARCHAR  PRIMARY KEY,    
                                                            EXECUTED_AT TIMESTAMP NOT NULL
                                                       );
                                                       """)
        if response is not None:
            print('Could not create tables in migrations database!')
            print(response)
            return False

        print('Migration database created successfully.')

    else:
        print('Migration database detected.')

    return True


def run_migrations():
    available_migrations = os.listdir('/database_migration/')
    print('Detecting migration scripts...')
    for file in available_migrations:
        if not file.startswith('migration-') or not file.endswith('.sql'):
            available_migrations.remove(file)
        else:
            print(file)

    print('Detecting unexecuted migrations..')
    executed_migrations = db_manager.execute_query('SELECT * FROM MIGRATION')

    executed_migrations_file_names = []
    for migration in executed_migrations:
        print(migration['file_name'])
        executed_migrations_file_names.append(migration['file_name'])

    unexecuted_migrations = list(set(available_migrations) - set(executed_migrations_file_names))

    if not unexecuted_migrations:
        return

    for migration in unexecuted_migrations:
        db_manager.execute_query_no_return('INSERT INTO MIGRATION VALUES (%s, %s)', (migration, datetime.datetime.now()))

    db_manager.close_connection()
    db_manager.initialize_connection(db_name=db_name,
                                     db_username=db_username, db_password=db_password)
    for migration in unexecuted_migrations:
        db_manager.execute_query_no_return(open(migration, 'r').read())


if __name__ == '__main__':
    check_migrations_db()
    run_migrations()

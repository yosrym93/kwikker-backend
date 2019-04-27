import psycopg2
import os
import datetime
import time
import sys
import natsort
import click

db_manager = None
db_username: str = None
db_password: str = None
db_name: str = None
db_host: str = None
db_port: int = None
migrations_db_name: str = None


def check_migrations_db():
    # Check if the migrations database exist
    print('Connecting to the migrations database..')
    response = db_manager.initialize_connection(db_name=migrations_db_name,
                                                db_username=db_username,
                                                db_password=db_password,
                                                host=db_host,
                                                port=db_port)
    if isinstance(response, psycopg2.OperationalError):
        # Migrations database does not exist, connect to the default database
        print('Migration database does not exist..')
        print('Connecting to the default (postgres) database..')
        response = db_manager.initialize_connection(db_name='postgres',
                                                    db_username=db_username,
                                                    db_password=db_password,
                                                    host=db_host,
                                                    port=db_port)
        if response is not None:
            print('Could not connect to postgres database!')
            print(response)
            return False

        print('Connected.')
        print('Creating migrations database..')
        db_manager.connection.autocommit = True
        response = db_manager.execute_query_no_return('CREATE DATABASE ' + migrations_db_name)
        db_manager.connection.autocommit = False

        if response is not None:
            print('Migrations database could not be created!')
            print(response)
            return False

        print('Migrations database created successfully, connecting to migrations database..')
        db_manager.close_connection()
        response = db_manager.initialize_connection(db_name=migrations_db_name,
                                                    db_username=db_username,
                                                    db_password=db_password,
                                                    host=db_host,
                                                    port=db_port)
        if response is not None:
            print('Could not connect to migrations database!')
            print(response)
            return False

        print('Connected. Creating schema..')
        response = db_manager.execute_query_no_return("""
                                                        CREATE TABLE MIGRATION(
                                                            FILE_NAME   VARCHAR  PRIMARY KEY,    
                                                            EXECUTED_AT TIMESTAMP NOT NULL
                                                       );
                                                       """)
        if response is not None:
            print('Could not create schema in migrations database!')
            print(response)
            return False

        print('Migration database created successfully.')

        # Check if the database was already existing without a migrations database, if so, delete it
        db_manager.connection.autocommit = True
        db_manager.execute_query_no_return('DROP DATABASE ' + db_name)
        db_manager.connection.autocommit = False

    elif response is not None:
        print('Error connecting to migrations database.')
        print(response)
        return False
    else:
        print('Migration database detected.')

    return True


def run_migrations():
    available_migrations = os.listdir(os.path.dirname(os.path.realpath(__file__)))

    print('Detecting migration scripts...')
    invalid_files = []
    for file in available_migrations:
        if not file.startswith('migration') or not file.endswith('.sql'):
            invalid_files.append(file)

    for file in invalid_files:
        available_migrations.remove(file)

    print('Detecting unexecuted migrations..')
    executed_migrations = db_manager.execute_query('SELECT * FROM MIGRATION')

    executed_migrations_file_names = []
    for migration in executed_migrations:
        executed_migrations_file_names.append(migration['file_name'])

    unexecuted_migrations = list(set(available_migrations) - set(executed_migrations_file_names))
    unexecuted_migrations = natsort.natsorted(unexecuted_migrations)

    if not unexecuted_migrations:
        print('No unexecuted migrations, your database schema is up to date!')
        return True

    print('Logging migrations...')
    for migration in unexecuted_migrations:
        response = db_manager.execute_query_no_return('INSERT INTO MIGRATION VALUES (%s, %s)',
                                                      (migration, datetime.datetime.now()))
        if response is not None:
            print('Problem logging migration:', migration)
            print(response)
            print('Please un-log any logged migrations manually.')
            return False

        print('Logging', migration, '..')

    db_manager.close_connection()

    print('Connecting to your database..')
    connected_to_database = True
    response = db_manager.initialize_connection(db_name=db_name,
                                                db_username=db_username,
                                                db_password=db_password,
                                                host=db_host,
                                                port=db_port)

    successful_migrations = True
    if response is not None:
        if isinstance(response, psycopg2.OperationalError):
            print('Your database is not created!')
            print('Connecting to migrations database..')
            db_manager.initialize_connection(db_name=migrations_db_name,
                                             db_username=db_username,
                                             db_password=db_password,
                                             host=db_host,
                                             port=db_port)
            print('Connected.')
            print('Creating your database..')
            db_manager.connection.autocommit = True
            db_manager.execute_query_no_return('CREATE DATABASE ' + db_name)
            db_manager.connection.autocommit = False
            print('Created.')
            print('Connecting to your database..')
            response = db_manager.initialize_connection(db_name=db_name,
                                                        db_username=db_username,
                                                        db_password=db_password,
                                                        host=db_host,
                                                        port=db_port)
            if response is not None:
                connected_to_database = False
            else:
                print('Connected.')
                print('Executing migrations..')
        else:
            connected_to_database = False

        if not connected_to_database:
            print('Could not connect to your database!')
            print(response)
            successful_migrations = False
            db_manager.initialize_connection(db_name=db_name,
                                             db_username=db_username,
                                             db_password=db_password,
                                             host=db_host,
                                             port=db_port)
    else:
        print('Executing migrations..')

    for migration in unexecuted_migrations:
        if successful_migrations:
            print('Executing', migration, '...')
            response = db_manager.execute_query_no_return(open(os.path.dirname(
                os.path.realpath(__file__)) + '/' + migration, 'r').read())
            if response is not None:
                print('Error executing migration', migration)
                print(response)
                successful_migrations = False
                print('Re-rolling logs..')
                print('Connecting to the migrations database..')
                response = db_manager.initialize_connection(db_name=migrations_db_name,
                                                            db_username=db_username,
                                                            db_password=db_password,
                                                            host=db_host,
                                                            port=db_port)
                if response is not None:
                    print('Could not connect to the migrations database, your migrations log is inconsistent.')
                    print(response)
                    print('Please update manually.')

                print('Un-logging', migration, '..')
                response = db_manager.execute_query_no_return('DELETE FROM MIGRATION WHERE FILE_NAME = %s',
                                                              (migration,))
                if response is not None:
                    print('Could not un-log', migration, '!')
                    print(response)
                    print('Please un-log manually')

        else:
            print('Un-logging', migration, '..')
            response = db_manager.execute_query_no_return('DELETE FROM MIGRATION WHERE FILE_NAME = %s',
                                                          (migration,))
            if response is not None:
                print('Could not un-log', migration, '!')
                print(response)
                print('Please un-log manually')

    if successful_migrations:
        print('Database migrated successfully.')
        return True
    else:
        print('Database migration failed!')
        return False


def register_migration(file_name):
    if not os.path.isfile(file_name):
        print('File does not exist.')
        return

    if not file_name.endswith('.sql'):
        print('Not a SQL file.')
        return

    new_file_name = 'migration' + str(int(time.time())) + '.sql'
    os.rename(file_name, new_file_name)
    print('Migration registered.')


@click.command()
@click.option('--test', is_flag=True)
def migrate(test):
    import database_manager
    from app import app
    import config

    if test:
        app.config.from_object(config.TestingConfig)
    else:
        app.config.from_object(config.ProductionConfig)

    global db_username
    global db_password
    global db_name
    global migrations_db_name
    global db_manager
    global db_host
    global db_port

    db_manager = database_manager.db_manager
    db_username = app.config['DATABASE_USERNAME']
    db_password = app.config['DATABASE_PASSWORD']
    db_name = app.config['DATABASE_NAME']
    migrations_db_name = app.config['MIGRATIONS_DATABASE_NAME']
    db_host = app.config['DATABASE_HOST']
    db_port = app.config['DATABASE_PORT']

    if check_migrations_db() and run_migrations():
        return 0
    else:
        raise SystemExit(1)


def migrate_non_cli(_db_username, _db_password, _db_name, _migrations_db_name, _db_host,
                    _db_port, _db_manager):
    global db_username
    global db_password
    global db_name
    global migrations_db_name
    global db_host
    global db_port
    global db_manager

    db_username = _db_username
    db_password = _db_password
    db_name = _db_name
    migrations_db_name = _migrations_db_name
    db_host = _db_host
    db_port = _db_port
    db_manager = _db_manager

    return check_migrations_db() and run_migrations()


@click.command()
@click.argument('file_name')
def register(file_name):
    register_migration(file_name)


@click.group()
def cli():
    pass


cli.add_command(migrate)
cli.add_command(register)

if __name__ == '__main__':
    sys.path.append('..')
    cli()

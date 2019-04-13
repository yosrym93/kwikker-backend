import pytest
import app
from database_manager import db_manager
import click

all_modules = ['timelines_and_trends', 'authentication_and_registration', 'notifications',
               'direct_messages', 'kweeks', 'users_profiles']


@click.command()
@click.option('--module', default='')
def cli(module):
    if module == '':
        modules = all_modules
    elif module in all_modules:
        modules = [module]
    else:
        print('Module does not exist.')
        raise SystemExit(-1)

    app.initialize(env='test')

    failed = False
    final_exit_code = 0

    for module in modules:
        db_manager.execute_query_no_return('DELETE FROM USER_CREDENTIALS; DELETE FROM HASHTAG;')
        db_manager.execute_query_no_return(open(module + '/seed.sql', 'r').read())
        exit_code = pytest.main(['--cov-report', 'term-missing', '--cov=' + module,
                                 module + '/test_actions.py'])
        if exit_code != 0 and not failed:
            failed = True
            final_exit_code = exit_code

    # db_manager.execute_query_no_return('DELETE FROM USER_CREDENTIALS; DELETE FROM HASHTAG;')
    raise SystemExit(final_exit_code)


if __name__ == '__main__':
    cli()
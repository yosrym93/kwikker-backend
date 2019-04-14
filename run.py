import app
import click

"""
    The application should be started by running this file from the terminal.
    To run in use:
        python run.py --env=<env>
        <env> = production , test, or dev (default is dev)
"""


@click.command()
@click.option('--env', default='dev')
def cli(env):
    app.run(env=env)


if __name__ == '__main__':
    cli()

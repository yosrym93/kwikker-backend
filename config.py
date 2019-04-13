"""
Add your custom configurations to config_local.py
Configurations on config_local.py overwrite the configurations in this file.
"""


class BaseConfig:
    RESTPLUS_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    DEBUG = True
    SECRET_KEY = 'kwikkerSecretKeyIsSALTS'
    CODE_KEY = 'kwikkerConfirmationCode'
    ERROR_404_HELP = False
    TESTING = False
    DATABASE_NAME = 'kwikker'
    DATABASE_USERNAME = 'postgres'
    DATABASE_PASSWORD = ''
    DATABASE_HOST = None
    DATABASE_PORT = 5432
    MIGRATIONS_DATABASE_NAME = 'migrations'
    SERVER_PATH = 'http://127.0.0.1:5000/'


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    DATABASE_USERNAME = 'kwikker'
    DATABASE_PASSWORD = '8Av5R7tRNqJSm4sXW23E'
    DATABASE_HOST = 'kwikker-database.cxappseoabsy.eu-central-1.rds.amazonaws.com'


class TestingConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = True
    DATABASE_NAME = 'kwikker_test'
    MIGRATIONS_DATABASE_NAME = 'migrations_test'

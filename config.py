class BaseConfig:
    RESTPLUS_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    DEBUG = True
    SECRET_KEY = 'kwikkerSecretKeyIsSALTS'
    ERROR_404_HELP = False
    TESTING = False
    DATABASE_NAME = 'kwikker'
    DATABASE_USERNAME = 'postgres'
    DATABASE_PASSWORD = ''
    MIGRATIONS_DATABASE_NAME = 'migrations'


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False


class TestingConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    TESTING = True
    DATABASE_NAME = 'kwikker_test'
    DATABASE_USERNAME = 'postgres'
    DATABASE_PASSWORD = ''
    MIGRATIONS_DATABASE_NAME = 'migrations_test'

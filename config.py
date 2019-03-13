class BaseConfig:
    RESTPLUS_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    DEBUG = True
    SECRET_KEY = ''
    DATABASE_NAME = ''
    DATABASE_USERNAME = ''
    DATABASE_PASSWORD = ''


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True


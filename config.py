class BaseConfig:
    RESTPLUS_MASK_SWAGGER = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    DEBUG = True
    SECRET_KEY = ''


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    DATABASE_NAME = ''
    DATABASE_USERNAME = ''
    DATABASE_PASSWORD = ''


class TestingConfig(BaseConfig):
    ENV = 'production'
    TESTING = True


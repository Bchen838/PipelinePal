import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pipelinepal.db'
    JWT_SECRET_KEY = 'a5fec00c1e5fe10239d1f53a6137669472022292c877addfe5556710caf872c3'


class ProductionConfig:
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith('postgres://'):
        uri = uri.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = uri
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
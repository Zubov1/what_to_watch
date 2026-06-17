import os


class Config(object):
    """Конфигурация what_to_watch."""

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY', '')

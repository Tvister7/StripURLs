import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-very-secret-key'
    REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_DB = os.environ.get('REDIS_DB') or 1

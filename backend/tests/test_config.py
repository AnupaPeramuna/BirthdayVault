import os
import secrets
from dotenv import load_dotenv
from config import Config



project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

basedir = os.path.abspath(os.path.dirname(__file__))

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI') or \
    'sqlite:///' + os.path.join(basedir, 'test_app.db')
    JWT_SECRET_KEY = os.environ.get('TEST_JWT_SECRET_KEY') or secrets.token_hex(32)


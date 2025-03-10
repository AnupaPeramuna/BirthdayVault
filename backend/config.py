import datetime
import os
import secrets
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
    JWT_TOKEN_LOCATION =  ["cookies"]
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_SAMESITE = "Lax"
    
    JWT_COOKIE_SECURE = False # True requires HTTPS
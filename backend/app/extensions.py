from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


# to resolve circular import errors
db = SQLAlchemy()
jwt = JWTManager()

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  

def create_app(config_class=Config):
    app = Flask(__name__)

    db.init_app(app)

    migrate = Migrate(app, db)  

    from app import routes, models  

    return app
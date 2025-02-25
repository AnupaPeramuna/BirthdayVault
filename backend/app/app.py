from flask import Flask, jsonify
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import User, TokenBlockList
from .extensions import db

import logging


jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logging.basicConfig(level=logging.ERROR)



    #initialize 
    db.init_app(app) 
    jwt.init_app(app)


    migrate = Migrate(app, db) 

    from .auth import auth_bp
    from .error_handler import error_bp

    #register blueprints
    app.register_blueprint(error_bp)
    app.register_blueprint(auth_bp)



    #load user
    @jwt.user_lookup_loader
    def user_loader_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.get_user_by_username(identity)
    
    #additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        return {"is_registered_user": True}
    
    #jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token is expired", "error": "token_expired"}), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "verificaiton failed", "error": "invaldi_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "No valid token", "error": "authorizaiton_required"}), 401 


    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data["jti"]
        token = TokenBlockList.query.filter_by(jti=jti).first()
        return token is not None

    return app
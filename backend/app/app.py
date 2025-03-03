from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.extensions import db, jwt
from app.users.models import User
from app.auth.models import TokenBlockList

import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logging.basicConfig(level=logging.ERROR)



    #initialize 
    db.init_app(app) 
    jwt.init_app(app)


    migrate = Migrate(app, db) 

    from app.auth.routes import auth_bp
    from app.utils.errors import error_bp

    #register blueprints
    app.register_blueprint(error_bp)
    app.register_blueprint(auth_bp)



    #load user
    @jwt.user_lookup_loader
    def user_loader_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.get_user_by_email(identity)
    
    #additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        return {"is_registered_user": True}
    
    #jwt error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"error": "token_expired"}), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "invalid token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({ "error": "authorization_required"}), 401 


    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data["jti"]
        token = TokenBlockList.query.filter_by(jti=jti).first()
        return token is not None

    return app
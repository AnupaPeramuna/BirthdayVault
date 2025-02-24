from flask import Blueprint, jsonify, request
from .models import User, TokenBlocklist
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post("/register")
def register_users():

    data = request.get_json()

    username = data.get('username')
    password_hash = data.get('password')
    user = User.get_user_by_username(username)

    if user is not None:
        return jsonify({"error": "User already exists"}, 409)

    new_user = User(username)
    new_user.set_password(password_hash)
    new_user.save()

    return jsonify({"message": "User created"}, 201)

    
@auth_bp.post('/login')
def login_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')
    user = User.get_user_by_username(username)

    if user and (user.check_password(password)):
        access_token = create_access_token(user.username)
        refresh_token = create_refresh_token(user.username)

        return jsonify(
            {
                "message": "Logged In",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token
                }
            }
        ), 200
    
    return jsonify({"error": "Invalid username or password"}),400


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token })

@auth_bp.get('/logout')
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_b = TokenBlocklist(jti=jti)
    token_b.save()

    return jsonify({"message": f"{token_type} token revoked succesffuly"}), 200

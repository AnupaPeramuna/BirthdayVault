import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app.auth.models import TokenBlockList
from app.users.models import User
from app.auth.utils import validate_user_input

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post("/register")
def register_users():

    try:
        data = request.get_json()

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        errors = validate_user_input(email, username, password)
        if errors:
            return jsonify({"error": errors}), 400


        user = User.get_user_by_email(email=email)
        if user is not None:
            return jsonify({"error": "User already exists"}), 409
        
        new_user = User(email = email, username=username)
        new_user.set_password(password=password)
        new_user.save()

        return jsonify({"message": "User created"}), 201
    
    except Exception as e:
        logging.error(f"Error registering user: {e}")
        raise 
    

@auth_bp.post('/login')
def login_user():

    try: 
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.get_user_by_email(email=email)

        if user and (user.check_password(password)):
            access_token = create_access_token(user.email)
            refresh_token = create_refresh_token(user.email)

            return jsonify(
                {
                    "message": "Logged In",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            ), 200
        
        return jsonify({"error": "Invalid email or password"}),400
    
    except Exception as e:
        logging.error(f"Error logging in user: {e}")
        raise


@auth_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh_token():

    try:
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return jsonify({"access_token": new_access_token })
    
    except Exception as e:
        logging.error(f"Error refreshing user access token: {e}")
        raise

@auth_bp.post('/logout')
@jwt_required(verify_type=False)
def logout_user():
    try:
        jwt = get_jwt()

        jti = jwt['jti']
        token_type = jwt['type']

        blocked_token = TokenBlockList(jti=jti)
        blocked_token.save()

        return jsonify({"message": f"{token_type} token revoked successfully"}), 200
  
    except Exception as e:
        logging.error(f"Error logging out user: {e}")
        raise
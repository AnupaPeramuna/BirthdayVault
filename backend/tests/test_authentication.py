import pytest
from app.extensions import db
from app.app import create_app
from app.users.models import User
from tests.test_config import TestConfig

@pytest.fixture
def client():
    try:
        app = create_app(config_class=TestConfig)
        with app.test_client() as client:
            with app.app_context():
                db.create_all()

                test_user = User(email = 'test_user_1@gmail.com', username='test_user_1')
                test_user.set_password('test_User_1_password!!')
                db.session.add(test_user)
                db.session.commit()

            yield client
            with app.app_context():
                db.session.delete(test_user)
                db.session.commit()

                db.drop_all()

    except Exception as e:
        pytest.fail(f"Error creating testing client: {e}")


def test_register_user(client):
    try:
        register_response = client.post('/auth/register', json={
            'email': 'test_user_2@gmail.com',
            'username': 'test_user_2',
            'password': 'test_User_2_password!!'
        })

        assert register_response.status_code == 201

        register_info = register_response.json

        assert 'message' in register_info
        
    except Exception as e:
        pytest.fail(f"Error testing user registration: {e}, Response json: {register_info}")


def test_register_user_no_email(client):
    try:
        register_response = client.post('/auth/register', json={
            'email': '',
            'username': 'test_user_2',
            'password': 'test_User_2_password!!'
        })

        assert register_response.status_code == 400

        register_info = register_response.json

        assert 'error' in register_info
        
    except Exception as e:
        pytest.fail(f"Error testing user registration with no email: {e}, Response json: {register_info}")


def test_register_user_no_username(client):
    try:
        register_response = client.post('/auth/register', json={
            'email': 'test_user_2@gmail.com',
            'username': '',
            'password': 'test_User_2_password!!'
        })

        assert register_response.status_code == 400

        register_info = register_response.json

        assert 'error' in register_info
        
    except Exception as e:
        pytest.fail(f"Error testing user registration with no username: {e}, Response json: {register_info}")


def test_register_user_no_password(client):
    try:
        register_response = client.post('/auth/register', json={
            'email': 'test_user_2@gmail.com',
            'username': 'test_user_2',
            'password': ''
        })

        assert register_response.status_code == 400

        register_info = register_response.json

        assert 'error' in register_info
        
    except Exception as e:
        pytest.fail(f"Error testing user registration with no password: {e}, Response json: {register_info}")


def test_register_user_email_taken(client):
    try:
        register_response = client.post('/auth/register', json = {
            'email':'test_user_1@gmail.com',
            'username': 'test_user_1_email_taken',
            'password':'test_User_2_password!!_email_taken'
        })

        assert register_response.status_code == 409
        
        register_info = register_response.json

        assert 'error' in register_info
        
    except Exception as e:
        pytest.fail(f"Error testing user registration where email taken: {e}, Response json: {register_info}")


@pytest.mark.parametrize("password", [
    "", # no password given
    "weak", # < 8 letters
    "1_weak_password", # no uppercase 
    "1_WEAK_PASSWORD", # no lowercase
    "_weak_Password_", # no digits
    "1WeakPassword", # no special characters
])
def test_register_user_weak_password(client, password):
    try:
        register_response = client.post('/auth/register', json = {
            'email': 'test_user_2@gmail.com',
            'username': 'test_user_2',
            'password': password
        })

        assert register_response.status_code == 400

        register_info = register_response.json

        assert 'error' in register_info
        
    except Exception as e:
        pytest.fail(f"Error testing user registration with weak password: {e}, Response json: {register_info}")


def test_login_user(client):
    try:
        login_response = client.post('/auth/login', json={
            'email': 'test_user_1@gmail.com',
            'password': 'test_User_1_password!!'
        })

        assert login_response.status_code == 200

        login_info = login_response.json

        assert 'message' in login_info
        assert 'token' in login_info
        assert 'access' in login_info['token']
        assert 'refresh' in login_info['token']

    except Exception as e:
        pytest.fail(f"Error testing login: {e}, Response json: {login_info}")


@pytest.mark.parametrize("password", [
    #similar to the actual password: 'test_user_2_password!!'
    "test_user_1_password!!",
    "test_User_2_password!!",
    "test_User_1_password!"

])
def test_login_user_invalid_password(client, password):
    try:
        login_response = client.post('/auth/login', json={
        'email': 'test_user_1@gmail.com',
        'password': password
        })

        assert login_response.status_code == 400

        login_info = login_response.json

        assert 'error' in login_info
    
    except Exception as e:
        pytest.fail(f"Error testing login with invalid password: {e}, Response json: {login_info}")


def test_refresh_access_token(client):
    try:
        # Login
        login_response = client.post('/auth/login', json={
        'email': 'test_user_1@gmail.com',
        'password': 'test_User_1_password!!'
        })

        assert login_response.status_code == 200

        login_info = login_response.json

        assert 'refresh' in login_info['token']
        refresh_token = login_info['token']['refresh']

        # Refresh token endpoint
        refresh_response = client.get('/auth/refresh', headers={'Authorization': f'Bearer {refresh_token}'})

        assert refresh_response.status_code == 200
        refresh_info = refresh_response.json
        assert 'access_token' in refresh_info

    except Exception as e:
        pytest.fail(f"Error testing refresh token: {e}, Response json: {refresh_info}")


def test_logout_user(client):
    try:
        # Login 
        login_response = client.post('/auth/login', json={
        'email': 'test_user_1@gmail.com',
        'password': 'test_User_1_password!!'
        })

        assert login_response.status_code == 200

        login_info = login_response.json

        assert 'access' in login_info['token']
        access_token = login_info['token']['access']

        # Logout
        logout_response = client.get('/auth/logout', headers={'Authorization': f'Bearer {access_token}'})

        assert logout_response.status_code == 200

        logout_info = logout_response.json
        assert 'message' in logout_info

    except Exception as e:
        pytest.fail(f"Error testing logout: {e}, Response json: {logout_info}")

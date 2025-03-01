import re

def validate_password(password):
    min_length = 8

    password_errors = []
    rules = [
        (len(password) < min_length, "Password must be at least 8 characters long."),
        (not re.search(r"[A-Z]", password), "Password must contain at least one uppercase letter (A-Z)."),
        (not re.search(r"[a-z]", password), "Password must contain at least one lowercase letter (a-z)."),
        (not re.search(r"\d", password), "Password must contain at least one digit (0-9)."),
        (not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."),
    ]

    for condition, message in rules:
        if condition:
            password_errors.append(message)

    return password_errors

def validate_user_input(email, username, password):
    errors = []

    if not email:
        errors.append("Please enter your email address")
    if not username:
        errors.append( "Please enter a username")
    
    if not password:
        errors.append("Please enter a password")
        return errors
    
    errors.extend(validate_password(password))

    return errors
         

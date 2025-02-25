import re

def validate_password(password):
    min_length = 8

    errors = []
    rules = [
        (len(password) < min_length, "Password must be at least 8 characters long."),
        (not re.search(r"[A-Z]", password), "Password must contain at least one uppercase letter (A-Z)."),
        (not re.search(r"[a-z]", password), "Password must contain at least one lowercase letter (a-z)."),
        (not re.search(r"\d", password), "Password must contain at least one digit (0-9)."),
        (not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."),
    ]

    for condition, message in rules:
        if condition:
            errors.append(message)

    return errors
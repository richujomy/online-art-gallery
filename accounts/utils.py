import re
from django.contrib.auth.models import User

def validate_signup(username, email, password1, password2):

    # Check required fields
    if not username or not email or not password1 or not password2:
        return "All fields are required."

    # Username validation
    if len(username) < 3:
        return "Username must be at least 3 characters long."
    
    if username.isdigit():
        return "Username cannot be entirely numeric."

    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        return "Username can only contain letters, numbers, and underscores."

    if User.objects.filter(username=username).exists():
        return "Username is already taken."

    # Email validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        return "Enter a valid email address."

    if User.objects.filter(email=email).exists():
        return "Email is already registered."

    # Password validation
    if password1 != password2:
        return "Passwords do not match."

    if len(password1) < 6:
        return "Password must be at least 6 characters long." 

    if not re.search(r"[A-Z]", password1):
        return "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password1):
        return "Password must contain at least one lowercase letter."

    if not re.search(r"\d", password1):
        return "Password must contain at least one digit."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password1):
        return "Password must contain at least one special character."

    return None

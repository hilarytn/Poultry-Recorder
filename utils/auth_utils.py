from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
import re

def hash_password(password):
    return generate_password_hash(password)

def generate_access_token(user_id):
    return create_access_token(identity=user_id)

def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
    return bool(re.match(pattern, password))

def generate_verification_token(user):
    token = create_access_token(identity=user.email, expires_delta=timedelta(hours=24))
    return token
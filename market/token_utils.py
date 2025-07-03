from itsdangerous import URLSafeTimedSerializer
import os

def get_serializer():
    secret = os.environ.get("SECRET_KEY", "dev-fallback")
    return URLSafeTimedSerializer(secret)

def generate_token(email):
    return get_serializer().dumps(email, salt='password-reset-salt')

def verify_token(token, expiration=3600):
    try:
        return get_serializer().loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None

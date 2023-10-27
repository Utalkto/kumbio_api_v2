"""Utils functions"""
# Django
from datetime import timedelta

import jwt
from django.conf import settings
from django.utils import timezone


def generate_auth_token(user, **kwargs):
    """Create JWT token that the user can use to login for specific context [origin]."""
    expiration_date = timezone.localtime() + timedelta(days=2)
    payload = {
        "user": user.email,
        # UTC format
        "exp": int(expiration_date.timestamp()),
        "type": "login",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def decode_auth_token(token, origin, skip_validation=False):
    """Decode JWT auth token based on origin."""
    error = []
    payload = ""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        except jwt.ExpiredSignatureError:
            error.append("Verification link has expired.")
    except jwt.PyJWTError:
        error.append("Invalid token")
    if not payload:
        error.append("Not payload")
    else:
        if not skip_validation:
            if payload["type"] != origin:
                error.append("Invalid origin jwt")
    return payload, error

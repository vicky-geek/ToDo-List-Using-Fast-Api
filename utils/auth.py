import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone


def encryptPass (password : str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def decryptPass (password : str, hashedPassword : str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashedPassword.encode('utf-8')) 


def _expires_at(duration: str | None) -> datetime:
    """Convert env value like 5m, 7d, 3600 into expiry datetime."""
    now = datetime.now(timezone.utc)
    if not duration:
        return now + timedelta(minutes=15)

    duration = duration.strip().lower()
    if duration.isdigit():
        return now + timedelta(seconds=int(duration))

    amount = int(duration[:-1])
    unit = duration[-1]
    if unit == "s":
        return now + timedelta(seconds=amount)
    if unit == "m":
        return now + timedelta(minutes=amount)
    if unit == "h":
        return now + timedelta(hours=amount)
    if unit == "d":
        return now + timedelta(days=amount)

    return now + timedelta(minutes=15)


def generateAccessToken (user : dict) -> str:
    jwt_secret = os.getenv('JWT_SECRET')    
    jwt_algorithm = os.getenv('JWT_ALGORITHM')
    payload = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "exp": _expires_at(os.getenv('ACCESS_TOKEN_EXPIRES_IN')),
    }
    print(" generateAccessToken payload :", payload)
    return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)


def generateRefreshToken (user : dict) -> str:
    jwt_secret = os.getenv('JWT_SECRET')    
    jwt_algorithm = os.getenv('JWT_ALGORITHM')
    payload = {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "exp": _expires_at(os.getenv('REFRESH_TOKEN_EXPIRES_IN')),
        "type": "refresh",
    }
    print(" generateRefreshToken payload :", payload)
    return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)

def verifyToken (token : str) -> dict | None:
    try:
        jwt_secret = os.getenv('JWT_SECRET')
        jwt_algorithm = os.getenv('JWT_ALGORITHM')
        return jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
    except jwt.InvalidTokenError:
        return None
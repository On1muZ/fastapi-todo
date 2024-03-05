from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status
from passlib.context import CryptContext
from config import Settings
import jwt


settings = Settings()
crypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def sign_jwt(username: str, user_id: UUID) -> str:
    now = datetime.utcnow()
    expire = now.utcnow() + timedelta(weeks=2)
    payload = {
        "sub": str(user_id),
        "username": username,
        "created_at": now.timestamp(),
        "expire": expire.timestamp()
    }
    token = jwt.encode(
        payload=payload,
        algorithm=settings.auth_jwt.ALGORITHM,
        key=settings.auth_jwt.SECRET
    )
    return token


def decode_jwt(token: str) -> dict:
    payload = jwt.decode(
        jwt=token,
        algorithms=[settings.auth_jwt.ALGORITHM],
        key=settings.auth_jwt.SECRET
    )
    if payload['expire'] > datetime.utcnow().timestamp():
        return payload
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token has been expired")


def get_password_hash(password: str) -> str:
    hashed_password = crypt_context.hash(password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(plain_password, hashed_password)

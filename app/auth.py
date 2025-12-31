"""Authentication features"""

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
import jwt
from datetime import timedelta, datetime, timezone
from typing import Annotated, Union

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

password_hash = PasswordHash.recommended()
SECRET_KEY = "7b64a2ad7c16f594ac0d9e8d185d63b18af6dfae4432c9e0da19f9c8c6d0082d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password):
    """Hashes provided password"""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Verified provided password and the hashed one"""
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(payload: dict, expires_delta: Union[timedelta, None] = None):
    """Created encoded JSON Web Token"""
    to_encode = payload.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def extract_payload_from_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    """Extracts payload from the JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception


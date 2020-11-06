from typing import Generator
from fastapi import Depends, HTTPException, status,Security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from crud import crud_user
import schemas
from core.config import settings
from db.database import SessionLocal
from core.role import scope

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/token", 
    scopes=scope.SCOPES
    )

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token,settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = schemas.token.TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = crud_user.get_user_by_username(db=db,user_name=username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user

async def get_current_active_user(
    current_user = Security(get_current_user, scopes=["ME"])
):
    if current_user.activate==False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_scopess(role):
    if role=="executor":
        return scope.EXECUTOR_SCOPESS
    elif role=="manager":
        return scope.MANAGER_SCOPESS
    return scope.ADMIN_SCOPESS



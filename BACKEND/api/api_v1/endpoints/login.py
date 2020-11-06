from schemas import token
from fastapi import APIRouter, Depends, HTTPException,status,Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from sqlalchemy.orm import Session
from core.config import settings
from core import sercurity
from crud import crud_user
from api import deps
from datetime import datetime, timedelta
import mysql.connector
import json
import requests as Request
router = APIRouter()

@router.post("/token", response_model= token.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(deps.get_db)):
    '''
    Login with web base account
    '''
    try:
        curent_user=crud_user.get_user_by_username(db,form_data.username)
        if curent_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username ",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token =sercurity.create_access_token(
            data={"sub": curent_user.user_name,
            "role":curent_user.role,
            "id":curent_user.id,
            "scopes":deps.get_scopess(curent_user.role)
            
            }, expires_delta=access_token_expires
        )
        crud_user.update_last_login(db=db,user_id=curent_user.id)
    except (mysql.connector.Error):
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="My sql connection error ",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/gmail/access-token")
async def login_with_google(google_token_id:str,db: Session = Depends(deps.get_db) ):
    '''
    Login with  gmail
    '''
    try:

        idinfo = json.loads(Request.get('https://oauth2.googleapis.com/tokeninfo?id_token='+google_token_id).text)
        if sercurity.check_email(idinfo["email"]) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email should be end with epsilo.io"
            ) 
        curent_user=crud_user.get_user_by_username(db=db,user_name=idinfo["email"])
        if curent_user is None :
            curent_user=crud_user.create_new_user(db=db,user_name=idinfo["email"],role="admin")

        crud_user.update_last_login(db=db,user_id=curent_user.id)
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token =sercurity.create_access_token(
            data={"sub": curent_user.user_name,
            "role":curent_user.role,
            "id":curent_user.id,
            "scopes":deps.get_scopess(curent_user.role)
            }, expires_delta=access_token_expires
        )
        
    except ValueError:
        raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="token id error ",
                headers={"WWW-Authenticate": "Bearer"},
            ) 
    pass
    return {"access_token": access_token,"token_type": "bearer"}



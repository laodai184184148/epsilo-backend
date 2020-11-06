from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import and_
from api import deps
from models import user
from schemas import user_schema

import random
from fastapi import APIRouter, Depends, HTTPException
import string


def get_user(db: Session, user_id: str):
    return db.query(user.User).filter(user.User.id == user_id).first()

def get_all_executor(db:Session):
    executors=db.query(user.User).filter(user.User.role=="executor").all()
    return executors

def get_all_manager(db:Session):
    managers=db.query(user.User).filter(user.User.role=="manager").all()
    return managers

def get_all_user(db: Session):
    return db.query(user.User).all()

def get_user_by_username(db: Session, user_name: str):
    user_db=db.query(user.User).filter(user.User.user_name == user_name).first()
    return user_db

def create_user(db: Session, users: user_schema.UserCreate):
    db_user = user.User(user_name=users.user_name, role=users.role,activate=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def inactivate_user(db:Session,user_id:str,activate:str):
    db.query(user.User).filter(user.User.id == user_id).update({user.User.activate:activate})
    db.commit()

def create_new_user(db:Session,user_name:str,role:str):
    db_user = user.User(user_name=user_name, role=role,activate=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_last_login(db:Session,user_id:str):
    db.query(user.User).filter(user.User.id == user_id).update({user.User.last_login:datetime.now()})
    db.commit()

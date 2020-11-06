from typing import Any, List,Optional
from fastapi import APIRouter, Depends, HTTPException,status,Security
from sqlalchemy.orm import Session
from crud import crud_user,crud_shop,crud_channel,crud_url,crud_sim_url,crud_sim
from schemas import user_schema,shop_schema,channel_schema
from api import deps
from core import sercurity
from schemas.exception import UnicornException
router = APIRouter()

@router.get("/", response_model=List[user_schema.User])
def All_users(
    current_user= Security(deps.get_current_active_user,scopes=["READ_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View All User
    '''
    return crud_user.get_all_user(db=db)


@router.get("/executors")
def All_executors(
    current_user= Security(deps.get_current_active_user,scopes=["READ_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View All executor User
    '''
    return crud_user.get_all_executor(db=db)

@router.get("/managers")
def All_managers(
    current_user= Security(deps.get_current_active_user,scopes=["READ_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View All manager User
    '''
    return crud_user.get_all_manager(db=db)
@router.post("/create_new_user", response_model=user_schema.User)
def Create_new_user(
    new_user:user_schema.UserCreate,
    current_user= Security(deps.get_current_active_user,scopes=["READ_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Create_new_user
    '''
    if sercurity.check_email(new_user.user_name) is False:
        raise UnicornException(
        messages="Invalid Email",
        name=new_user.user_name
         )
    if not crud_user.get_user_by_username(db=db,user_name=new_user.user_name) is None:
        raise UnicornException(messages="Email already exist",name=new_user.user_name)
    if new_user.role not in['executor','manager']:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid Role"
        )
    return crud_user.create_user(db=db,users=new_user)
@router.get("/{id}", response_model=user_schema.User)
def user_detail(
    id:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View user detail  with user id 
    '''
    return crud_user.get_user(db=db,user_id=id)

@router.post("/{id}/inactivate")
def Inactivate_user(
    id:str,
    current_user= Security(deps.get_current_active_user,scopes=["INACTIVATE_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Inactivate user
    '''
    crud_user.inactivate_user(db=db,user_id=id,activate="0")
    return {"message":"Inactivate success"}



@router.post("/{id}/activate")
def activate_user(
    id:str,
    current_user= Security(deps.get_current_active_user,scopes=["INACTIVATE_USER"]),
    db: Session = Depends(deps.get_db)
):
    '''
    Activate user
    '''
    crud_user.inactivate_user(db=db,user_id=id,activate="1")
    return {"message":"Activate success"}



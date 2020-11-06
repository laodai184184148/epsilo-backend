from typing import List,Optional
from pydantic import BaseModel, ValidationError
from fastapi import APIRouter, Depends,Header,Security
from sqlalchemy.orm import Session
from crud import crud_channel,crud_shop,crud_user
from api import deps
from schemas.exception import UnicornException
router = APIRouter()

@router.get("/")
def View_all_channel(
    current_user= Security(deps.get_current_active_user,scopes=["READ_CHANNEL"]),
    db: Session = Depends(deps.get_db)
):
    '''
        Get all channel
    '''
    return crud_channel.get_all_channel_db(db=db)


@router.get("/{channel_id}")
def View_Channel_Details(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_CHANNEL"]),
    db: Session = Depends(deps.get_db)
):
    '''
        View Channel details
    '''
    if crud_channel.get_channel(db=db,channel_id=channel_id) is None:
        raise UnicornException(
        messages="CHANNEL ID NOT FOUND",
        name=channel_id
        )
    return crud_channel.get_channel(db=db,channel_id=channel_id)

@router.get("/{channel_id}/shops")
def View_All_shop_of_channel(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_CHANNEL"]),
    db: Session = Depends(deps.get_db)
):
    '''
        View All Shop of channel
    '''
    if crud_channel.get_channel(db=db,channel_id=channel_id) is None:
        raise UnicornException(
        messages="CHANNEL ID NOT FOUND",
        name=channel_id
        )
    return crud_shop.get_all_shop_channel(db=db,channel_id=channel_id)


@router.get("/{channel_id}/shop-count")
def Count_shop_of_channel(
    channel_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_CHANNEL"]),
    db: Session = Depends(deps.get_db)
):
    if crud_channel.get_channel(db=db,channel_id=channel_id) is None:
        raise UnicornException(
        messages="CHANNEL ID NOT FOUND",
        name=channel_id
        )
    return crud_shop.count_shop(db=db,channel_id=channel_id)


    
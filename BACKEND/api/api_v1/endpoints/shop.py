from typing import List

from fastapi import APIRouter, Depends,status,Security
from sqlalchemy.orm import Session
from core.config import settings
from crud import crud_shop,crud_user,crud_sim,crud_shop_sim
from schemas import shop_schema,sim_schema,user_schema
from api import deps
from schemas.exception import UnicornException
router = APIRouter()

@router.get("/",response_model=List[shop_schema.Shop])
def View_All_shop(
    skip: int = 0,
    limit: int = 100,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SHOP"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View All Shop
    '''
    return crud_shop.get_all_shops(db, skip=skip, limit=limit)

@router.get("/{shopid}", response_model=shop_schema.Shop)
def View_Shop_detail(
    shopid:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SHOP"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View Shop detail 
    '''
    if crud_shop.get_shop(db=db,shop_id=shopid) is None:
        raise UnicornException(
            messages="SHOP ID NOT FOUND",
            name=shopid
            )
    return crud_shop.get_shop(db=db,shop_id=shopid)

@router.get("/{shop_id}/all-sim",response_model=List[sim_schema.Sim])
def View_all_sim_of_shop(
    shop_id:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SHOP"]),
    db: Session = Depends(deps.get_db)
):
    '''
    View All sim of shop
    '''
    if crud_shop.get_shop(db=db,shop_id=shop_id) is None:
        raise UnicornException(
            messages="SHOP ID NOT FOUND",
            name=shopid
            )
    return crud_sim.get_all_sim_of_shop(db=db,shop_id=shop_id)


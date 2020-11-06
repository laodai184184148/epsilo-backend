from fastapi import APIRouter, Depends,Header,status,Security
from typing import Any, List,Optional
from sqlalchemy.orm import Session
from datetime import datetime
from crud import crud_sim,crud_message,crud_shop_sim,crud_shop,crud_url,crud_user,crud_tag
from schemas import sim_schema,message_schema
from api import deps
from schemas.exception import UnicornException
router = APIRouter()



@router.get("/")
def View_all_sim(
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    return crud_sim.get_all_sim(db=db)

@router.get("/{sim_number}")
def View_Sim_Details(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    if crud_sim.get_sim_by_number(db=db,sim_number=sim_number) is None:
        raise UnicornException(
            messages="SIM NOT FOUND",
            name=sim_number
        )
    return crud_sim.get_sim_by_number(db=db,sim_number=sim_number)

@router.get("/{sim_number}/shops")
def View_all_shop_of_an_sim(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    if crud_sim.get_sim_by_number(db=db,sim_number=sim_number) is None:
        raise UnicornException(
            messages="SIM NOT FOUND",
            name=sim_number
        )
    return crud_shop.get_all_shop_of_sim(db=db,sim_number=sim_number)

@router.get("/{sim_number}/all-messages")
def View_all_messages_of_an_sim(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    if crud_sim.get_sim_by_number(db=db,sim_number=sim_number) is None:
        raise UnicornException(
            messages="SIM NOT FOUND",
            name=sim_number
        )
    return crud_sim.get_message(db=db,sim_number=sim_number)

@router.get("/{sim_number}/shop-count")
def count_shop_of_sim(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    if crud_sim.get_sim_by_number(db=db,sim_number=sim_number) is None:
        raise UnicornException(
            messages="SIM NOT FOUND",
            name=sim_number
        )
    return crud_shop_sim.count_shop_sim(db=db,sim_number=sim_number)

@router.get("/{sim_number}/url")
def view_All_url_asigned_to_an_sim(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    if crud_sim.get_sim_by_number(db=db,sim_number=sim_number) is None:
        raise UnicornException(
            messages="SIM NOT FOUND",
            name=sim_number
        )
    return crud_url.get_all_url_of_sim(db=db,sim_number=sim_number)

@router.get("/{sim_number}/not_url")
def View_all_url_not_asigned_to_an_sim(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    if crud_sim.get_sim_by_number(db=db,sim_number=sim_number) is None:
        raise UnicornException(
            messages="SIM NOT FOUND",
            name=sim_number
        )
    return crud_url.get_all_urlnot_of_sim(db=db,sim_number=sim_number)

@router.get("/{sim_number}/all_tag")
def View_all_tag_of_sim(
    sim_number:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    return crud_tag.tags_of_sim(db=db,sim_number=sim_number)


@router.post("/add_tag")
def Add_tag_to_sim(
    sim_number:List[str],
    tag_title:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_SIM"]),
    db: Session = Depends(deps.get_db)
):
    for s in sim_number:
        crud_tag.create_tag(db=db,sim_number=s,title=tag_title)

    return {"message":"create success"}










from fastapi import APIRouter, Depends,Header,status,Security
from sqlalchemy.orm import Session
from crud import crud_tag
from schemas import sim_schema,message_schema
from api import deps
from schemas.exception import UnicornException
router = APIRouter()


@router.get("/")
def View_all_tag(
    current_user= Security(deps.get_current_active_user,scopes=["URL"]),
    db: Session = Depends(deps.get_db)
):
    return crud_tag.tags(db=db)

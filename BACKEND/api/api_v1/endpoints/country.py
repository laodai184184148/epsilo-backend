from fastapi import APIRouter, Depends,Security
from sqlalchemy.orm import Session
from crud import crud_country,crud_shop
from schemas import country_schema
from api import deps
from schemas.exception import UnicornException
router = APIRouter()




@router.get("/")
def View_all_Countries(
    current_user= Security(deps.get_current_active_user,scopes=["READ_COUNTRY"]),
    db: Session = Depends(deps.get_db)
):
    '''
        View All Country
    '''
    return crud_country.get_all_country(db=db)

@router.get("/{postal_code}", response_model=country_schema.Country)
def View_country_detail(
    postal_code:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_COUNTRY"]),
    db: Session = Depends(deps.get_db)
):
    '''
        View Country Details
    '''
    if crud_country.get_country(db=db,country_id=postal_code) is None:
        raise UnicornException(
            messages="COUNTRY ID NOT FOUND",
            name=postal_code
            )
    return crud_country.get_country(db=db,country_id=postal_code)

@router.get("/{postal_code}/all_shop")
def View_All_Shop_Of_Country(
    postal_code:str,
    current_user= Security(deps.get_current_active_user,scopes=["READ_COUNTRY"]),
    db: Session = Depends(deps.get_db)
):
    '''
        View ALL Shop Of Country
    '''
    if crud_country.get_country(db=db,country_id=postal_code) is None:
        raise UnicornException(
            messages="COUNTRY ID NOT FOUND",
            name=postal_code
            )
    return crud_shop.get_all_shop_country(db=db,postal_code=postal_code)

    
from sqlalchemy.orm import Session
from sqlalchemy import update
from models import shop
from crud import crud_shop,crud_channel,crud_country,crud_shop_sim
from schemas import shop_schema

def get_shop(db: Session, shop_id: str):
    s= db.query(shop.Shop).filter(shop.Shop.id == shop_id).first()
    s.channel_name=crud_channel.get_channel(db=db,channel_id=s.channel_id).name
    s.country_name=crud_country.get_country(db=db,country_id=s.postal_code).name
    return s

def get_all_shops(db: Session, skip: int = 0, limit: int = 100):
    shops=db.query(shop.Shop).offset(skip).limit(limit).all()
    for s in shops:
        s.channel_name=crud_channel.get_channel(db=db,channel_id=s.channel_id).name
        s.country_name=crud_country.get_country(db=db,country_id=s.postal_code).name
        s.number_of_sim=crud_shop_sim.count_sim_of_shop(db=db,shop_id=s.id)
    return shops


def count_shop(db:Session,channel_id:str):
    return db.query(shop.Shop).filter(shop.Shop.channel_id == channel_id).count()

def count_shop_country(db:Session,postal_code:str):
    return db.query(shop.Shop).filter(shop.Shop.postal_code == postal_code).count()

def get_all_shop_channel(db:Session,channel_id:str):
    shops= db.query(shop.Shop).filter(shop.Shop.channel_id==channel_id).all()
    for s in shops:
        s.channel_name=crud_channel.get_channel(db=db,channel_id=s.channel_id).name
        s.country_name=crud_country.get_country(db=db,country_id=s.postal_code).name
    return shops

def get_all_shop_country(db:Session,postal_code:str):
    return db.query(shop.Shop).filter(shop.Shop.postal_code==postal_code).all()

def get_all_shop_of_sim(db:Session,sim_number:str):
    shop_ids=crud_shop_sim.get_all_shop_of_sim(db=db,sim_number=sim_number)
    shops=[]
    for id in shop_ids:
        shops.append(get_shop(db=db,shop_id=id[0]))
    return shops
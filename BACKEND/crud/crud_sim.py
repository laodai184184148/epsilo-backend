from sqlalchemy.orm import Session
from datetime import datetime
from crud import crud_shop_sim
from models import sim,message
from schemas import sim_schema

def get_all_sim(db: Session):
    sims= db.query(sim.Sim).all()
    for sim_object in sims:
        if (not sim_object.expire_date is None) and (not sim_object.expire_date ==""):
            sim_object.expire_date=datetime.strptime(sim_object.expire_date, "%d/%m/%Y").strftime("%m/%d/%Y")
    return sims

def get_sim(db: Session,tty_gateway:str):
    return db.query(sim.Sim).filter(sim.Sim.tty_gateway == tty_gateway).first()

def get_sim_by_number(db: Session, sim_number: str):
    return db.query(sim.Sim).filter(sim.Sim.sim_number ==sim_number ).first()

def get_all_sim_of_shop(db:Session,shop_id:str):
    sim_number_list=crud_shop_sim.get_all_shop_sim(db=db,shop_id=shop_id)
    sims=[]
    for id in sim_number_list:
        sims.append(id[0])
    return db.query(sim.Sim).filter(sim.Sim.sim_number.in_(sims) ).all()


def get_message(db:Session,sim_number:str):
    return db.query(message.Message).filter(message.Message.phone_owner==sim_number).all()

def count_shop(db:Session,sim_number:str):
    return db.query(sim.Sim).filter(sim.Sim.sim_number ==sim_number ).count()



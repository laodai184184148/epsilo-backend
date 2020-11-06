from sqlalchemy.orm import Session
from sqlalchemy import not_
from models import url
from crud import crud_sim_url

def create_new_url(db: Session, new_url:str):
    db_url = url.Url(url=new_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url(db:Session,id:str):
    return db.query(url.Url).filter(url.Url.id==id).first()

def find_url(db:Session,input_url:str):
    return db.query(url.Url).filter(url.Url.url==input_url).first()
def get_all_url(db:Session):
    urls= db.query(url.Url).all()
    for u in urls:
        u.number_of_sim=crud_sim_url.count_sim_of_url(db=db,url_id=u.id)
    return urls
 
def delete_url(db:Session,id:str):
    db.query(url.Url).filter(url.Url.id==id).delete()
    db.commit()

def update_url(db:Session,id:str,new_url:str):
    db.query(url.Url).filter(url.Url.id==id).update({url.Url.url: new_url})
    db.commit()

def get_all_url_of_sim(db:Session,sim_number:str):
    url_id=crud_sim_url.get_url_id_of_sim(db=db,sim_number=sim_number)
    url_id_list=[]
    for id in url_id:
        url_id_list.append(id.url)
    return db.query(url.Url).filter(url.Url.id.in_(url_id_list)).all()

def get_all_urlnot_of_sim(db:Session,sim_number:str):
    url_id=crud_sim_url.get_url_id_of_sim(db=db,sim_number=sim_number)
    url_id_list=[]
    for id in url_id:
        url_id_list.append(id.url)
    return db.query(url.Url).filter(url.Url.id.notin_(url_id_list)).all()

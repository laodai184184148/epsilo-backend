from sqlalchemy.orm import Session
from datetime import datetime
from models import tag

def create_tag(db:Session,sim_number:str,title:str):
    tag_db=tag.Tag(sim_number=sim_number,title=title)
    db.add(tag_db)
    db.commit()
    db.refresh(tag_db)
    return tag_db

def tags(db:Session):
    return db.query(tag.Tag).all()

def tags_of_sim(db:Session,sim_number:str):
    tags= db.query(tag.Tag).filter(tag.Tag.sim_number==sim_number).all()
    if tags ==[]:
        return [{"sim_number":sim_number}]
    return tags
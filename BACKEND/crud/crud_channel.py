from sqlalchemy.orm import Session
from crud import crud_shop
from models import channel
from schemas import channel_schema

def get_channel(db: Session, channel_id: str):
    return db.query(channel.Channel).filter(channel.Channel.id == channel_id).first()

def get_all_channel_db(db: Session):
    channels=db.query(channel.Channel).all()
    for c in channels:
        c.number_of_shop=crud_shop.count_shop(db=db,channel_id=c.id)
    return channels

def create_channel(db: Session, created_channel: channel_schema.ChannelCreate):
    db_channel = channel.Channel(id=created_channel.id,name=created_channel.name)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


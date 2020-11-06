
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Shop_sim(Base):
    __tablename__ = "shop_sim"
    shop_id = Column(String(45), primary_key=True)
    sim_number  = Column(String(45), primary_key=True)


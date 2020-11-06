
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from db.base_class import Base

class Country(Base):
    __tablename__ = "country"
    postal_code = Column(String(45), primary_key=True)
    name  = Column(String(45))  


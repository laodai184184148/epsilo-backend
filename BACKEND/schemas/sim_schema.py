from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class SimBase(BaseModel):
    sim_number:str


class SimCreate(SimBase):
    tty_gateway: str
    status:str


class Sim(SimBase):
    tty_gateway:Optional[str] = None
    status:Optional[str] = None
    balance:Optional[float] = None
    expire_date:Optional[date] = None
    
    expire_date:Optional[str] = None
    balance :Optional[float] = None
    check:Optional[bool] = None

    class Config:
        orm_mode = True
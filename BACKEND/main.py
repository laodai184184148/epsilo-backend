from typing import List
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Request, Response,status
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
from api.api_v1.api import api_router
from api import deps
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from core.config import settings
import crud
from core import sercurity
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
import asyncio
from schemas import exception
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from provider import vietnamobile, viettel, vinaphone, mobifone, sim_processing, error_handler, end_point, thread_processing
import serial, os, time, re, queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from fastapi_utils.tasks import repeat_every


app = FastAPI(
    title="laodais"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
@app.exception_handler(exception.UnicornException)
async def unicorn_exception_handler(request: Request, exc: exception.UnicornException):
    return JSONResponse(
        status_code=502,
        content={"message": f"{exc.messages}: {exc.name}"}
    )
######################################################
sim = sim_processing
######################################################

@app.on_event("startup")
def declare_list_Device():
    print("starting...")
    end_point.open_port()

@app.on_event("startup")
@repeat_every(seconds=10) #10 secs
def check_incomming_sms():
    if settings.repeat:
        t = Thread(target=end_point.check_messages, args=(settings.list_Device,))
        settings.main_Thread.append(t)
        t.start()
        t.join()
        settings.main_Thread.pop(settings.main_Thread.index(t))
        print("===============")

######################################################
@app.get("/sim/check-sim",tags=["sim"])
def Check_Sim():
    res = []
    for Device in settings.list_Device:
        res.append({Device.status["port"].name:Device.data["phone_number"]})
    return ({"available":res})

@app.get("/sim/balance-all",tags=["sim"])
def Check_balance_all_sim():
    if settings.repeat:
        t = Thread(target=end_point.check_balances, args=(settings.list_Device,))
        settings.main_Thread.append(t)
        t.start()
        t.join()
        settings.main_Thread.pop(settings.main_Thread.index(t))
    return{"status":"done"}

@app.post("/sim/balance-manual",tags=["sim"])
def check_Balance_manual(list_Phone:List[str]):
    if settings.repeat:
        t = Thread(target=end_point.check_balance_manually, args=(list_Phone,settings.list_Device,))
        settings.main_Thread.append(t)
        t.start()
        t.join()
        settings.main_Thread.pop(settings.main_Thread.index(t))
    return{"status":"done"}


@app.get("/sim/refresh-sim",tags=["sim"])
def refresh_all_sim():
    settings.repeat = False
    t = Thread(target=end_point.open_port)
    settings.main_Thread.append(t)
    while not(thread_processing.check_ready(t.getName(),settings.main_Thread)):
        pass
    t.start()
    print("sim refreshing...")
    t.join()
    settings.main_Thread.pop(0)
    settings.repeat = True
    return{"status":"done"}


app.include_router(api_router)
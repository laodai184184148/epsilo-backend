from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import queue, time

from provider import vietnamobile, viettel, vinaphone, mobifone, sim_processing, error_handler, thread_processing
from core.config import settings

from db.database import SessionLocal
from models import sim as sim_model

#declare
sim = sim_processing
gateway = error_handler.Cinterion
db = SessionLocal()
#class device informaiton
list_Device = []

#open all port for gsm
def open_port():
    db.query(sim_model.Sim).update({sim_model.Sim.status:False})
    db.commit()
    old_list_Device = settings.list_Device
    list_port_url = sim.gsm_name()
    thread_list = []
    exe = ThreadPoolExecutor()
    new_list_Device=[]
    for port_url in list_port_url:
        t = exe.submit(sim.open_single_port, port_url)
        thread_list.append(t)
    for n in thread_list:
        Device = n.result()
        if Device != False:
            new_list_Device.append(Device)
    #compare with old device
    for nD in new_list_Device:
        if nD.data["phone_number"] != False:
            for oD in old_list_Device:
                if nD.status["port"].name == oD.status["port"].name and nD.data["phone_number"] == oD.data["phone_number"]:
                    nD = oD
                ''' else:
                    #delete all message before working
                    for i in range(1,41):
                        nD.status["port"].write('AT+CMGD={}\r'.format(i).encode())
                        time.sleep(0.5) '''
    #db process
    for nD in new_list_Device:
        if db.query(sim_model.Sim).filter(sim_model.Sim.sim_number == str(nD.data["phone_number"])).first() == None:
            db_sim = sim_model.Sim(
                            sim_number = str(nD.data["phone_number"]),
                            tty_gateway  = str(nD.status["port"].name),
                            status = True   ,
                            expire_date="",
                            balance = None,
                            check="False"
                            )
            db.add(db_sim)
            db.commit()
        else:
            db.query(sim_model.Sim).filter(sim_model.Sim.sim_number == str(nD.data["phone_number"])).update({sim_model.Sim.status:True})
            db.commit()
    settings.list_Device = new_list_Device
#check message
def check_messages(list_Device):
    thread_list = []
    for Device in list_Device:
        t = Thread(target= sim.check_message_t(Device),args = (Device,))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
#check balance
def check_balances(list_Device):
    db.query(sim_model.Sim).update({sim_model.Sim.check:"checking"})
    db.commit()
    data = []
    q = queue.Queue()
    thread_list = []
    for Device in list_Device:
        t = Thread(target= lambda queue,Device : queue.put(sim.check_balance(Device)),args=(q,Device,))
        thread_list.append(t)
        t.start()
    for t in thread_list:
        t.join()
    for t in thread_list:
        r = q.get()
        print("-------------")
        print(r)
        data.append(r)
    return {"status":"done"}
#check balance manually
def check_balance_manually(list_Phone, list_Device):
    data = []
    q = queue.Queue()
    thread_list = []
    for Device in list_Device:
        for phone in list_Phone:
            if Device.data["phone_number"] == phone:
                db.query(sim_model.Sim).filter(sim_model.Sim.sim_number == str(Device.data["phone_number"])).update({sim_model.Sim.check:"checking"})
                db.commit()
                t = Thread(target= lambda queue,Device : queue.put(sim.check_balance(Device)),args=(q,Device,))
                thread_list.append(t)
                t.start()
    for t in thread_list:
        t.join()
    for t in thread_list:
        r = q.get()
        print("-------------")
        print(r)
        data.append(r)
    return {"status":"done"}
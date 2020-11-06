from provider import sim_processing, error_handler
import re, time
from core.config import settings

sim = sim_processing
#check balance
def expired(Device):
    return balance(Device)

#get phone number
def get_num(Device):
    #Device - status: port
    #                 tries
    #                 gateway
    port = Device.status["port"]
    tries = Device.status["tries"]
    gateway = Device.status["gateway"]
    #
    script = 'AT+CUSD=1,"*123#",15\r'
    res = sim.get_data(script,port,tries,gateway)
    if res["status"] == True:
        result = re.findall("[0-9]+",res["data"][0].decode("utf-8",errors="ignore"))[1]
        return result
    else:
        return(False)

#input money
def recharge(port,code):
    script='AT+CUSD=1,"*100*{}#",15\r'.format(code)
    res = sim.port_write(port,script)
    for r in res:
        r = r.decode("utf-8", errors = "ignore")
        text = text+"\n"+r
    if text == "":
        return({"Response":"errors"})
    else:
        return({"Response":text})

#expired date
def balance(Device):
    script='AT+CUSD=1,"*101#",15\r'
    tries = Device.status["tries"]
    port = Device.status["port"]
    tries = Device.status["tries"]
    gateway = Device.status["gateway"]
    date = ""
    balance = ""
    indexs = []
    while True:
        res = sim.get_data(script, port, tries, gateway)
        if res["status"] == True:
            break
        time.sleep(1)
    res = res["data"]
    for n in range(60):
        for r in res:
            r = r.decode("utf-8",errors="ignore")
            for SIGNAL in settings.SMS_SIGNAL:
                if(SIGNAL in r):
                    index = re.findall("[0-9]+",r)[0]
                    print(Device.data["phone_number"]+": "+index)
                    indexs.append(index)
        for index in indexs:
            script = "AT+CMGR={}\r".format(index)
            res = sim.get_message(Device, index)
            for r in res:
                r = r.decode("utf-8",errors="ignore").strip("\n")
                #ident expire date and main balance
                if "TK Chinh: "in r:
                    balance = re.findall("[0-9]",r)
                    if len(balance) != 0:
                        balance = str(balance[0])
                if "het han" in r:
                    date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)
                    if len(date) != 0:
                        date = str(date[0])
                #done
        time.sleep(1)
        res = port.readlines()
    return ({"phone_number":Device.data["phone_number"],
             "data":{"date":date,
                     "balance":balance}})
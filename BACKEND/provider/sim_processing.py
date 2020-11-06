import time, re, requests, json, serial, os, queue
import mysql.connector
from threading import Thread
from core.config import settings
from provider import vinaphone, mobifone, viettel, vietnamobile, error_handler, thread_processing

from db.database import SessionLocal
from models import message
from models import sim as sim_model

providers = settings.providers
gateway = error_handler.Cinterion
db = SessionLocal()
#port#
#open mysql connection
def connection():
    cnx = mysql.connector.connect(user=settings.MYSQL_USER, 
                                    password=settings.MYSQL_PASSWORD,
                                    host=settings.MYSQL_SERVER,
                                    database=settings.MYSQL_DB,
                                    auth_plugin=settings.AUTH_PLUGIN)
    return cnx
#execute query 
def get_info(q):
    cnx = connection()
    cursor = cnx.cursor()
    cursor.execute(q)
    if q.split()[0].upper()=="SELECT":
        r = cursor.fetchall();
        cnx.close()
        cursor.close()
        return(r)
    else:
        cnx.commit()
        cnx.close()
        cursor.close()
#check signal in realtime
def check_signal(port):
    r = 0
    while r == 0:
        r = port.inWaiting()
    time.sleep(2)
#write script into port
def port_write(port,script:str):
    port.write(script.encode())
    check_signal(port)
    res = port.readlines()
    return(res)

#trying to get response in tries time
def get_data(script,port,tries:int,cb=None):
    while tries > 0 :
        res = port_write(port, script)
        #print all res
        """ for r in res:
            print(r.decode("utf-8",errors = "ignore").strip("\n")) """
        metadata = error_handler.is_error(res)
        if metadata["status"] == True:
            break
        tries = tries-1
        time.sleep(1)
    if tries == 0:
        return ({"status":False})
    else:
        res = cb(res,metadata["type"])
    return ({"status":True,
            "data":res})
#check provider
def check_provider(port):
    while True:
        str = 'AT+CIMI\r'
        res = port_write(port, str)
        if res != []:
            break
    res = res[1].decode("utf-8", errors="ignore")[0:5]
    if providers[res] == "vinaphone":
        return(vinaphone)
    elif providers[res] == "mobifone":
        return(mobifone)
    elif providers[res] == "viettel":
        return(viettel)
    elif providers[res] == "vietnamobile":
        return(vietnamobile)
#get message-------------------------
def get_message(Device, index):
    script = "AT+CMGR={}\r".format(index)
    port = Device.status["port"]
    tries = Device.status["tries"]
    gateway = Device.status["gateway"]
    res = get_data(script,port, tries,gateway)["data"]
    info = sms_info(res)
    raw_sms = ""
    for r in res:
        if res.index(r) != 0:
            r = r.decode("utf-8", errors="ignore").strip("\n")
            raw_sms = raw_sms + r
    otp = get_otp(Device,res)
    if otp == "":
        print("message is stored without otp")
    else:
        print("message is stored with otp: "+otp)
    #db process
    q = "insert into  message (phone_owner, time ,otp  ,raw_message,from_number ,date,shop_id ) values(\""+Device.data["phone_number"]+"\",\""+info["time"]+"\",\""+otp+"\",\""+raw_sms+"\",\""+info["phone"]+"\",\""+info["date"]+"\",\"\");"
    get_info(q)
    isfull(port,index)
    return(res)
#check sim store full or not and remove all messages when full
def isfull(port,index):
    index = int(index)
    if index > 30:
        for i in range(index+1):
            port.write('AT+CMGD={}\r'.format(i).encode())
            time.sleep(0.5)
    else:
        return False
#check and get otp:
def get_otp(Device, res:list):
    otp = ""
    #handle raw responses
    decode_res = []
    for r in res:
        decode_res.append(r.decode("utf-8",errors="ignore").strip("\n"))
    decode_res.pop(0)
    #
    for r in decode_res:
        if len(re.findall('\d{6}', r))!=0:
            otp = re.findall('\d{6}', r)[0]
            break
    """ if otp != "":
        passport_url = "https://api-staging-passport.epsilo.io/receive-otp/shopee"
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        passport_payload = "{\"phone\": \"" + Device.data["phone_number"] + "\", \"otp\": \"" + otp + \
                                           "\", \"timestamp\": \"" + time_stamp + "\"}"
        passport_headers = {
            'accept': "application/json",
            'cache-control': "no-cache"
        }
        passport_response = connect_with_retry(passport_url, passport_payload, passport_headers)
        print("passport_response: ", passport_response)
        passport_response_error_code = int(passport_response["response_code"])
        error_message = passport_response["response_message"]
        slack_url = settings.SLACK_URL[1]
        slack_headers = {
            'accept': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        if passport_response_error_code == 1:
            print("send success")
            passport_response_data = dict(passport_response["response_data"])
            shop_name = passport_response_data["shopName"]
            country = passport_response_data["country"]
            slack_payload = "{\"channel\": \"#alert-otp\", \"text\": \"\n>Phone number: " \
                            + Device.data["phone_number"] + "\n>OTP: *" + otp + "*\n>Time: " + time_stamp \
                            + "\n>Shop: " + shop_name + "\n>Country: " + country + "\n>\"}"
        else:
            print("send failed")
            slack_payload = "{\"channel\": \"#alert-otp\", \"text\": \"\n>Phone number: " \
                + Device.data["phone_number"] + "\n>OTP: *" + otp + "*\n>Time: " + time_stamp \
                + "\n>Error: " + error_message + "\n>\"}"
        print("slack_url", slack_url, "slack_payload", slack_payload, "slack_headers", slack_headers)
        response_slack = requests.request("POST", slack_url, data=slack_payload
                                                           , headers=slack_headers)
        print(response_slack.text) """
    return otp
#check expire date:
def is_expired(res:list):
    date = []
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if len(re.findall("[0-9]+/[0-9]+/[0-9]+",r))!=0:
            date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)
            break
    if date == []:
        return ("")
    else:
        return date[0]
#get message infor
def sms_info(res:list):
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if "+CMGR:" in r:
            phone = r.split("\"")
            if len(phone)==0:
                phone = re.findall("[0-9]+",r)[0]
            else:
                phone = phone[3]
            date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)[0]
            time = re.findall("[0-9]+:[0-9]+:[0-9]+",r)[0]
            return ({"phone":phone,
                     "date":date,
                     "time":time})

#try to send request to server
def connect_with_retry(url, payload, headers):
    retry = 3
    response = {}
    while retry > 0:
        try:
            response = requests.request("POST", url, data=payload,
                                        headers=headers)
        except requests.exceptions.RequestException:
            print("Connect to passport failed, retrying...")
            retry = retry - 1
            time.sleep(40)
        else:
            break
    data_parse = parse_response(response)
    print("try: ", retry, "data_parse: ", data_parse)
    if retry > 0 and int(data_parse["response_code"]) == 0:
        zero_code_retry_times = 3
        while zero_code_retry_times > 0:
            print("zero code, retrying...")
            response = requests.request("POST", url, data=payload, headers=headers)
            data_parse = parse_response(response)
            if data_parse["response_code"] == 1:
                break
            else:
                zero_code_retry_times = zero_code_retry_times - 1
            # time.sleep(40)
    return data_parse
#parse res
def parse_response(response):
    error_message = ""
    error_code = 0
    data = []
    print(response.text)
    if hasattr(response, 'text'):
        try:
            response_data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            error_code = 500
            error_message = "Something wrong with Passport server"
        else:
            error_code = int(response_data["code"])
            error_message = response_data["message"]
            data = response_data["data"]
    return {
        "response_code": error_code,
        "response_message": error_message,
        "response_data": data
    }
#get gsm name
def gsm_name():
    result = os.popen('ls -al /dev/ | awk \'{print $10}\'').read()
    result =result.split("\n")
    list_path = []
    for r in result:
        for gsm_name in settings.GSM_NAME:
            if gsm_name in r:
                list_path.append(r)
    return (list_path)


#single
#get port
def open_single_port(port_url):
    class Device():
        data = {}
        status = {}
    t = 0
    path = "/dev/{}".format(port_url)
    port = serial.Serial(path, 9600, timeout=2)
    while t<3:
        port.write("ATI\r".encode())
        time.sleep(float(0.1+t+t))
        res = port.readlines()
        if len(res) != 0:
            break
        else:
            t += 1
    if t<3:
        Device.status.update({"port" : port})
        Device.status.update({"provider":check_provider(port)})
        Device.status.update({"cThread":[]})
        Device.status.update({"tries":settings.tries})
        Device.status.update({"gateway":gateway})
        Device.data.update({"phone_number":Device.status["provider"].get_num(Device)})
        print(port.name+" : "+str(Device.data["phone_number"]))
        return Device
    else:
        print("---> error port: "+port.name)
        return False
#function check message on a sim
def check_message_f(Device):
    port = Device.status['port']
    signal = port.readlines()
    print("checking : "+port.name)
    if len(signal)>0:
        for element in signal:
            element = element.decode("utf-8",errors="ignore").strip("\n").split(",")
            for SIGNAL in settings.SMS_SIGNAL:
                if(SIGNAL == element[0]):
                    index = element[1]
                    print(Device.data["phone_number"]+": "+index)
                    get_message(Device,index)
#thread check message in sim queue
def check_message_t(Device):
    t = Thread(target= check_message_f(Device),args = (Device,))
    Device.status["cThread"].append(t)
    if thread_processing.check_ready(t.getName(),Device.status["cThread"]) == True:
        pass
    t.start()
    t.join()
    Device.status["cThread"].pop(0)
#check balance on a sim
def check_balance(Device):
    data = ""
    while True:
        q = queue.Queue()
        t = Thread(target= lambda queue,Device : queue.put(Device.status["provider"].balance(Device)),args=(q,Device,))
        Device.status["cThread"].append(t)
        if thread_processing.check_ready(t.getName(),Device.status["cThread"]) == True:
            pass
        t.start()
        t.join()
        data = q.get()
        Device.status["cThread"].pop(0)
        if data!="" and data!=None:
            break
    

    if data["data"]["balance"] == "":
        query ="update sim set sim.check = \"False\" where sim_number = \""+data["phone_number"]+"\";"
        get_info(query)
    else:
        query ="update sim set sim.check = \"checked\", balance = "+data["data"]["balance"]+", expire_date = \""+data["data"]["date"]+"\" where sim_number = \""+data["phone_number"]+"\";"
        get_info(query)
    return data
from core.config import settings

def is_error(data):
    res = []
    for r in data:
        #r = r.strip("\n")
        r = r.decode("utf-8",errors="").strip("\n")
        res.append(r)
    for r in res:
        for item in settings.ERRORS_CODE:
            if item in r:
                return {"status":False}
    if len(res)!=0:
        if res[0] == res[len(res)-1] or res[1] == res[len(res)-1]:
            return {"status":False}
    #check type of data
        if "OK" in res[len(res)-1]:
            return {"status":True,
                    "type":"MEM"}
        else:
            return {"status":True,
                    "type":"USSD"}
    else:
        return {"status":False}

def Cinterion(data,type):
    if "USSD" in type:
        data.pop(0)
        data.pop(0)
        data.pop(0)
    if "MEM" in type:
        data.pop(0)
        data.pop(len(data)-1)
        data.pop(len(data)-1)
    return data
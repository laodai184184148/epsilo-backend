from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time

def check_ready(name:str,cThread:list):
    while True:
        time.sleep(0.2)
        if (cThread[0].getName() == name):
            break
    return True    
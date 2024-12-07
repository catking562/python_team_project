import time;
import threading

control = []
isStop = False

lock = threading.Lock();


def add_input(value):
    global isStop;
    global control;
    
    lock.acquire();
    if isStop:
        return False;
    
    control.append(value)
    lock.release()
    return True

def get_save():
    global control
    return control
    

def start():
    global isStop;
    global control
    
    control = [];
    isStop = False;
    return True;

def stop():
    global isStop;
    isStop = True;
    return True;

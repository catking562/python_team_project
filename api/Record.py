import time;
import threading

control = ()
isStop = False

lock = threading.Lock();

def add_input(value):
    global isStop;
    global control;
    
    lock.acquire();
    if isStop:
        return False;
    
    control += (value,)
    lock.release()
    return True

def get_save():
    global control
    return control
    

def start():
    global isStop;
    global control
    
    isStop = False;
    startTime = time.perf_counter;
    control += (startTime, )
    return True;

def stop():
    global isStop;
    isStop = True;
    return True;

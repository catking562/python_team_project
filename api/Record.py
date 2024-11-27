import time;
import threading

control = ()
isStop = False
startTime = 0

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

def start():
    global isStop;
    global startTime;
    global control
    
    isStop = False;
    startTime = time.perf_counter;
    control += (startTime, )
    return True;

def stop():
    global isStop;
    isStop = True;
    return True;

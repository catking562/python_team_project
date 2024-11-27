import time;
import threading

control = ()
isStop = False
startTime = 0

lock = threading.lock();

def getStartTime():
    StartTime = time.perf_counter
    return startTime;

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
    isStop = False;
    startTime = time.perf_counter;
    return True;

def stop():
    global isStop;
    isStop = True;
    return True;

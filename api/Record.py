import time;
import threading

control = ()
isStop = False
startTime = 0

lock = threading.lock();

#프로그램 시작 시간 저장
def getStartTime():
    StartTime = time.perf_counter  #시간 단위:s
    return startTime;

#입력 저장
def add_input(value):
    global isStop;
    global starttime
    global control;
    
    lock.acquire();
    if isStop:
        return False;
    
    control += (value,)
    lock.release()
    return True

def start():
    global isStop;
    global starttime;
    isStop = False;
    startTime = time.perf_counter;
    return True;

def stop():
    global isStop;
    isStop = True;
    return True;

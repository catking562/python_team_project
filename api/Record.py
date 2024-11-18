import time;

dictionary = {}
isStop = False;
startTime = 0;

def getNow():
    return round(time.time() * 1000);

def getStartTime():
    return startTime;

def getSaves():
    return dictionary;

def add_input(value):
    if isStop:
        return False;
    #dictionary에 입력 저장
    return True

def start():
    isStop = False;
    return True;

def stop():
    isStop = True;
    return True;
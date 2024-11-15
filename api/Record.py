dictionary = {}
isStop = False;

def getSaves():
    return dictionary;

def add_input(time, value):
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
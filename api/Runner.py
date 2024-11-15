isStop = False;

def start(dictionary):
    isStop = False;
    #dictionary에 들어있는 행동들을 반복
    while not isStop:
        print("반복중"); #이 줄은 삭제
    return True;

def repeatStart(dictionary):
    isStop = False;
    #dictionary에 들어있는 행동들을 무한반복
    while not isStop:
        print("반복중") #이 줄은 삭제
    return True;

def stop():
    isStop = True;
    return True;
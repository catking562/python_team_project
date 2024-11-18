"""
참고사항: 받은 dictionary데이터는
{<다음동작까지 걸리는 시간>:<다음 동작>}
형태로 이루어져 있음
"""

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
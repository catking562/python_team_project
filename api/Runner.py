"""
참고사항: 받은 dictionary데이터는
{<다음동작까지 걸리는 시간>:<다음 동작>}
형태로 이루어져 있음
"""
# 직접 생성
from pynput.keyboard import Controller
#pynput의 keyboard모듈에 Controller 라는 클래스를 불러옴

mouse=Controller()
#control.type("hello World")
#my_tuple = ((3,mouse.position=500,500),(2,"love"),(2,"정우"))


isStop = False

def start(tup):
    global isStop
    isStop = False
    #tuple에 들어있는 행동들을 반복
    for i in range(0,len(tup)):
            pg.sleep(tup[i][0])
            if isStop:
                return True
            #print(tup[i][1])


def stop():
    isStop = True
    return isStop

#start(my_tuple)


def repeatStart(tup):
    isStop = False
    while not isStop: #isstop이 참일 경우 while 루프를 벗어나도록 함
      for i in range(0,len(tup)):
            pg.sleep(tup[i][0])
            if isStop: #도중에 정지버튼을 누르면 정지하도록 함
                return True
            #print(tup[i][1])
    return True

#repeatStart(my_tuple)

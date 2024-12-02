from pynput.mouse import Controller, Button
from pynput.keyboard import Controller,Key
import time

# Mouse Controller 초기화
mouse = Controller()

my_tuple=((1,'click',Button.left,True),(1,'scroll',1,3,2,4),(2,'press0',Key.enter))
isStop = False
#tuple에 들어있는 행동들을 반복
def start(tup):
    global isStop , i
    isStop = False
    for i in my_tuple:
        time.sleep(i[0])
        case(i[1])

        if isStop:
            return True
        


def stop():
    isStop = True
    return isStop

#start(my_tuple)


def repeatStart(tup):
    isStop = False
    while not isStop: #isstop이 참일 경우 while 루프를 벗어나도록 함
      for i in range(0,len(tup)):
            time.sleep(tup[i][0])
            if isStop: #도중에 정지버튼을 누르면 정지하도록 함
                return True
    return True


def case(n):
    if n == "click":
        type_press = i[1]
        button = i[2]
        pressed = i[3]
        return type_press,button,pressed
    
    elif n == "scroll":
        type_press = i[1]
        x = i[2]
        y= i[3]
        dx = i[4]
        dy = i[5]
        return type_press , x, y , dx , dy
    elif n == "press0":
        type_press = i[1]
        key = i[2]
        return type_press , key

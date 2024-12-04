from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

# 마우스와 키보드 컨트롤러 초기화
mouse = Controller()
keyboard = KeyboardController()


my_tuple = [
    (1, 'click', Button.left, True),  
    (1, 'scroll', 1, 3, 2, 4),       
    (2, 'press0', Key.enter)          
]

isStop = False  

#반복 시작
def start(tup):
    global isStop  
    isStop = False
    for i in tup:
        time.sleep(i[0])  
        type_case(i)  
        if isStop:
            return True

# 반복을 멈추는 함수
def stop():
    global isStop
    isStop = True

# 행동 처리 함수
def type_case(action):
    if action[1] == "click":
        type_press = action[1]
        button = action[2]
        pressed = action[3]
        if pressed==True:
            mouse.press(button)
        else:
            mouse.release(button)
        #return type_press , button , pressed

    elif action[1] == "scroll":
        type_press = action[1]
        x = action[2]
        y = action[3]
        dx = action[4]
        dy = action[5]
        mouse.scroll(dx, dy)
        #return type_press , x, y, dx, dy

    elif action[1] == "press0":
        type_press = action[1]
        key = action[2]
        keyboard.press(key)
        keyboard.release(key)
        #return type_press, key

# 반복적으로 실행하는 함수
def repeatStart(tup):
    global isStop  
    while not isStop:
        for i in tup:
            time.sleep(i[0])  
            type_case(i)  
            if isStop:
                return True

start(my_tuple)


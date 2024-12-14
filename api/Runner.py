"""
참고사항: 받은 dictionary데이터는
{<다음동작까지 걸리는 시간>:<다음 동작>}
형태로 이루어져 있음
"""
# 직접 생성
from pynput.keyboard import Controller
#pynput의 keyboard모듈에 Controller 라는 클래스를 불러옴
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

# 마우스와 키보드 컨트롤러 초기화
mouse = Controller()
keyboard = KeyboardController()

""" 
my_list = [
    (1, 'click', Button.left, True),  
    (1, 'scroll', 1, 3, 2, 4),       
    (2, 'press0', Key.enter)          
]
"""
isStop = False  

#반복 시작
def start(lst):
    global isStop  
    isStop = False
    for i in tup:
        time.sleep(i[0])  
        type_case(i)  
        if isStop:
            return True

# 반복을 멈추는 함수 thread를 통해 다른 파이썬 파일에 의해 멈추는 기능 포함
def stop():
    global isStop
    isStop = True

# 행동 처리 함수
def type_case(action):
    if action[1] == "click":
        type_press = action[1]
        x = action[2];
        y = action[3];
        button = action[4]
        pressed = action[5]
        mouse.position = (x, y)
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
        mouse.position = (x, y)
        mouse.scroll(dx, dy)
        #return type_press , x, y, dx, dy

    elif action[1] == "press":
        type_press = action[1]
        key = action[2]
        keyboard.press(key)
        
        #return type_press, key
    elif action[1] == "release":
        type_press = action[1];
        key = action[2];
        keyboard.release(key);

# 반복적으로 실행하는 함수
def repeatStart(lst):
    global isStop;
    isStop = False;
    while not isStop: 
        for i in lst:
            time.sleep(i[0])  
            type_case(i)  
            if isStop:
                return True

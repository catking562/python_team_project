import time;
import threading

#입력받은 키보드 및 마우스 값을 저장할 리스트
control = []
#프로그램의 종료와 실행을 결정하는 변수
isStop = False

#키보드와 마우스를 인식하는 pynput의 Listener는 클래스 객채로, 내부에 스레드를 만듦.
#따라서 마우스와 키보드의 입력을 받아오는 스레드가 2개 이상 존재함.
#밑에 있는 lock은 두 개 이상의 스레드가 동시에 들어와서 데이터 저장 오류를 일으키는 것을 막기 위한 잠금장치
lock = threading.Lock();


#입력되는 키보드와 마우스의 데이터를 받아서 control의 리스트에 저장.
"""
value의 형식
마우스 클릭 및 드래그의 경우: [파이썬 실행으로부터의 시간, "click", x좌표, y좌표, 누른 버튼(좌클릭, 우클릭), 누른 상태]
마우스 스크롤 : [파이썬 실행으로부터의 시간, "scroll", x좌표, y좌표, 스크롤 하면서 움직인 x변화량, 스크롤 하면서 움직인 y변화량]
키보드 누르기 : [파이썬 실행으로부터의 시간, "press", 누른 키]
키보드 떼기 : [파이썬 실행으로부터의 시간, "press", 뗀 키]
"""
def add_input(value):
    global isStop;
    global control;
    
    #2개 이상의 스레드가 들어와 데이터 훼손을 막기 위한 코드
    #1개의 스레드가 들어오면 그 다음 스레드가 들어오지 못하게 막는다.
    lock.acquire();
    if isStop:
        return False;
    
    #control 리스트에 위와 같은 값을 가진 리스트를 넣는다.
    #control은 이차원 리스트
    control.append(value)
    #다른 스레드가 들어오는 걸 막는 잠금을 푼다.
    lock.release()
    return True

#이 함수를 부르면 control을 건내준다.
def get_save():
    global control
    return control
    
#녹화 시작 버튼을 눌러 녹화 모드로 변경이 된다면 시작되는 함수.
#이 함수에서 데이터를 저장할 control을 초기화하고, isStop을 초기값으로 바꾼다.
def start():
    global isStop;
    global control
    
    control = [];
    isStop = False;
    return True;

#녹화 종료 버튼을 눌러 녹화 종료 모드로 변경이 된다면 시작되는 함수.
#isStop을 True로 바꾸어 다른 함수에서 if문에 막히게 된다.
def stop():
    global isStop;
    isStop = True;
    return True;



from pynput.keyboard import Controller #Controller: 들어온 데이터를 출력
#pynput의 keyboard모듈에 Controller 라는 클래스를 불러옴
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KeyboardController, Key
import time

# 마우스와 키보드 컨트롤러 초기화
mouse = Controller() 
keyboard = KeyboardController()
#반복시작 키를 계속 누른 상태라면 stop키도 동시에 눌러지는 것을 방지
press_set = set()
#행동 예시
my_list = [
    [1, 'click', Button.left, True],  #[시간간격 , 행위, 버튼양식 , 버튼이 눌러있는 경우]
    [1, 'scroll', 1, 3, 2, 4],        #[시간간격 , 행위, x , y , x변화량, y변화량]
    [2, 'press0', Key.enter]         #[시간간격 , 행위 , 키 입력 종류]
]
#현재 Stop이 False로 초기화 :Stop비활성화 상태
isStop = False  

#반복 시작 함수 : 녹화된 리스트 값을 1번 반복
def start(lst):
    global isStop   #stop 비활성화 시킴으로써 반복 활성
    isStop = False
    for i in lst: #녹화된 중첩 리스트에서 하나의 리스트를 가져옴
        time.sleep(i[0])   #리스트의 첫번째 값에는 시간이 들어있기때문에 출력
        type_case(i)   #type_case함수로 넘겨받아서 행위 구분 및 실행
        if isStop: #녹화중지가 된 경우 (Stop이 활성화 된 경우)
            for i in press_set: #press_set에 남아있는 값을 때도록 함
                keyboard.release(i);
                
            return True

# 반복을 멈추는 함수
def stop():
    global isStop
    isStop = True #반복을 멈추는 경우 isStop이 True가 되면서 Stop이 활성화가 된다

# 행동 처리 함수 (반복 함수에서 리스트들을 하나씩 가져옴)
def type_case(action): 
    global press_set
    if action[1] == "click": #클릭한 경우
        steps = 1/1000  # 드래그를 부드럽게 하기 위한 단계 수
        #각 리스트에 들어있는 값들을 저장 
        type_press = action[1] : #클릭행위
        x = action[2]; #x,y의 좌표값
        y = action[3];
        button = action[4] #좌클릭 or 우클릭
        pressed = action[5] #눌렀는지를 bool형으로 저장
        
        
        if pressed==True: #눌려져 있는 경우
            mouse.position = (x, y) #저장된 좌표값들에 대하여 마우스 위치 이동
            mouse.press(button) #버튼 클릭(좌클릭 or 우클릭)
            
        else: #눌려져 있지 않는 경우 
            for i in range(1000):
                # 중간 위치 계산하여 가운데로 클릭
                current_x = x + action[6] * steps * i
                current_y = y + action[7] * steps * i
                mouse.position = (current_x, current_y)
                
            mouse.position = (x, y)
            mouse.release(button)
        #return type_press , button , pressed
         #스크롤한 경우
    elif action[1] == "scroll":
        type_press = action[1] 
        x = action[2] #각각의 위치값을 저장
        y = action[3]
        dx = action[4] #x값과 y값의 변화량 저장
        dy = action[5]
        mouse.position = (x, y) #출력
        mouse.scroll(dx, dy)
        #return type_press , x, y, dx, dy 

         #키를 누른 경우
    elif action[1] == "press":
        type_press = action[1] 
        key = action[2] #무슨 키를 눌렀는지 저장
        press_set.add(action[2])  #만약 키를 계속 누른 상태라면, press_set의 set형태로 저장
            
        keyboard.press(key) #키를 누름 
        #return type_press, key

        #키를 땐 경우
    elif action[1] == "release":
        type_press = action[1];
        key = action[2];
        press_set.discard(action[2]) #press_set에 들어있는 값을 버림
        keyboard.release(key); #키 값을 땐다

# 반복적으로 실행하는 함수 (반복종료 버튼을 누를 때까지 무한 반복)
def repeatStart(lst):
    global isStop; 
    isStop = False;
    while not isStop: #isStop이 False인 경우 무한반복 : 반복종료 버튼을 누를 때까지를 의미
        for i in lst: 
            time.sleep(i[0]) 
            type_case(i)  
            if isStop: #stop버튼을을 누른경우
                for i in press_set: #release를 거치치 않는 press_set의 값은 남아있기 떄문에 따로 처리
                    keyboard.release(i)
                return True

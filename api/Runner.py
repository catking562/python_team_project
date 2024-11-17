import pyautogui as pg


"""
참고사항: 받은 dictionary데이터는
{<다음동작까지 걸리는 시간>:<다음 동작>}
형태로 이루어져 있음
"""
# 직접 생성
my_dict = {'name': 'Alice', 'age': 25 , 'gender' : 'female'}



isStop = False

def start(dictionary):
    isStop = False
    #dictionary에 들어있는 행동들을 반복
    while not isStop:
        for i in dictionary.values():
            print(i) #i를 출력 검사 : 여기다가 행동 넣을 듯

            pg.sleep(1)
        return True


start(my_dict)

def repeatStart(dictionary):
    isStop = False;
    #dictionary에 들어있는 행동들을 무한반복
    while not isStop:
        for i in dictionary.values():
            print(i) #i를 출력 검사 : 여기다가 행동 넣을 듯

            pg.sleep(1)
        return True;

def stop():
    isStop = True
    return True

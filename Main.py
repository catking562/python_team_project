import tkinter;
from pynput.keyboard import Listener as kl;
from pynput.mouse import Listener as ml;

"""입력 이벤트들"""
#마우스 클릭 이벤트
def on_click(x, y, button, pressed):
    print(x, y, button, pressed);

#마우스 스크롤 이벤트
def on_scroll(x, y, dx, dy):
    print(x, y, dx, dy);

#키보드 다운 이벤트
def on_press(key):
    print(key);

#키보드 업 이벤트
def on_release(key):
    print(key);

"""GUI이벤트들"""
def initWindow(win):
    win.title("매크로");

"""초기화 시작"""
win = tkinter.Tk();
initWindow(win);

with ml(on_click=on_click, on_scroll=on_scroll) as listener:
    with kl(on_press=on_press, on_release=on_release) as listener:
        win.mainloop();
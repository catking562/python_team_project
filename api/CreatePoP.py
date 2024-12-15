import glob
import tkinter;
from pynput import keyboard

encording_pop = None;
input_value = "";
input_field = None;
buttons = None;
pop = None;

isNeedButton = False;

def destroy():
    global encording_pop;
    encording_pop.destroy();
    encording_pop = None;

def createMessage(message):
    global encording_pop;
    encording_pop = tkinter.Toplevel();
    encording_pop.title(message);
    encording_pop.geometry("200x100");
    tkinter.Label(encording_pop, text = message).pack(pady=20);

def filename_pop_accept():
    global encording_pop;
    global input_field
    global input_value;
    input_value = input_field.get();
    encording_pop.destroy();

def getFileName(win):
    global encording_pop;
    global input_value;
    global input_field;
    #생성
    input_value = "";
    encording_pop = tkinter.Toplevel();
    encording_pop.title("파일 이름 입력");
    encording_pop.geometry("200x80");
    tkinter.Label(encording_pop, text = "파일 이름을 입력하세요.").pack(pady=0);
    input_field = tkinter.Entry(encording_pop, width=10);
    input_field.pack(pady=0);
    tkinter.Button(encording_pop, text="확인", command=filename_pop_accept).pack(pady=5);
    encording_pop.grab_set();
    win.wait_window(encording_pop);
    input_field = None;
    encording_pop = None;
    return input_value;

def setButton(key):
    global input_value;
    global isNeedButton;
    input_value = str(key);
    isNeedButton = False;

def closeMiniPop():
    global pop;
    pop.destroy();

def detect_single_key():
    global input_value;
    global isNeedButton;
    input_value = "";
    isNeedButton = True;

def isneedButton():
    global isNeedButton;
    return isNeedButton;

def setOption(option, key, num):
    global buttons;
    global input_value;
    global pop;
    global encording_pop;
    for button in buttons:
        button['state']=tkinter.DISABLED;
    #창을 하나 더... ㅡㅡ
    pop = tkinter.Toplevel();
    pop.title("키 입력");
    pop.geometry("200x100");
    tkinter.Label(pop, text = "설정 할 키를 입력해 주세요.").pack(pady=20);
    #키 감지
    detect_single_key();
    encording_pop.wait_window(pop);
    option[key] = input_value;
    #복구
    for button in buttons:
        button['state']=tkinter.NORMAL;
    buttons[num]['text'] = str(input_value);

def editOption(option, win):
    global encording_pop;
    global buttons;
    encording_pop = tkinter.Toplevel();
    encording_pop.title("설정");
    encording_pop.geometry("300x"+str(30*len(option)));
    buttons = [];
    a = 0;
    for key in option:
        tkinter.Label(encording_pop, text = key).place(x=0, y=30*a);
        button = tkinter.Button(encording_pop, text=str(option[key]), command=lambda k=key, num=a:setOption(option, k, num));
        buttons.append(button);
        button.place(x=100, y=30*a, width=200, height=30);
        a=a+1;
    win.wait_window(encording_pop);

def returnSelect(r):
    global encording_pop;
    global input_value;
    input_value = r;
    encording_pop.destroy();

def getSelectInList(list, win):
    global encording_pop;
    global input_value;
    encording_pop = tkinter.Toplevel();
    encording_pop.title("파일 불러오기");
    encording_pop.geometry("300x"+str(30*len(list)));
    a = 0;
    for file in list:
        button = tkinter.Button(encording_pop, text = file, command=lambda r=file:returnSelect(r));
        button.place(x=0, y=30*a, width = 300, height=30);
        a=a+1;
    win.wait_window(encording_pop);
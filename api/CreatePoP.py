import tkinter;
from pynput import keyboard

encording_pop = None;
input_value = "";
input_field = None;
buttons = None;
pop = None;

isNeedButton = False;

"""파괴"""
#GUI를 파괴하는 함수
def destroy():
    global encording_pop;
    encording_pop.destroy();
    encording_pop = None;

"""메세지"""
#메세지를 보내는 용도(인코딩중 또는 저장중일 때)
def createMessage(message):
    global encording_pop;
    encording_pop = tkinter.Toplevel();
    encording_pop.title(message);
    encording_pop.geometry("200x100");
    tkinter.Label(encording_pop, text = message).pack(pady=20);

"""저장 할 때 파일이름 가져오기"""
#getFileName함수에서 생성한 GUI에서 버튼이 만들어지는데, 이 버튼을 클릭했을 때 이 함수가 실행됨
def filename_pop_accept():
    global encording_pop;
    global input_field
    global input_value;
    input_value = input_field.get();
    encording_pop.destroy();

#함수를 실행하면, 입력창이 나오고, 확인 버튼을 누르면 입력한 값을 반환(return)해줍니다.
#X를 눌러서 창을 닫으면 None이 반환되고, 이 경우에는 파일이 저장되지 않습니다.
def getFileName(win):
    global encording_pop;
    global input_value;
    global input_field;
    #생성
    input_value = None;
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

"""단축키를 설정 할 때"""
#버튼 데이터를 설정하는 함수.
#Main에서 키입력을 받았을 때, 메인으로부터 값을 받아올 때 사용함.
def setButton(key):
    global input_value;
    global isNeedButton;
    input_value = str(key);
    isNeedButton = False;

#setButton(ky) 함수가 발동되고 나서 실행됨. (Main에서 setButton(key)함수와 함께 실행함.)
#pop.destroy()가 발동되므로서 pop이라는 팝업창이 삭제되고, wait_window가 풀리면서 계속 진행되는 방식
def closeMiniPop():
    global pop;
    pop.destroy();

#setButton과 closeMiniPop() 함수로 값을 입력받기 전에, 초기화 시켜줌.
def detect_single_key():
    global input_value;
    global isNeedButton;
    input_value = "";
    isNeedButton = True;

#Main에서 키 데이터를 보내줘야 하는지 알려주는 용도.
#키 데이터가 필요하면 1을 반환함.
def isneedButton():
    global isNeedButton;
    return isNeedButton;


#editOption에서 만든 GUI의 버튼을 누르면 실행되는 함수
#Main으로부터 키를 입력해달라고 시킨 이후, Main으로부터 입력키를 받아온 다음에 option변수(hotkeys)에 반영
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

#이 함수가 실행되면, 설정버튼을 눌렀을 때 나오는 팝업창이 뜨고, 그 팝업창이 닫힐 때까지 유지 시켜줌.
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

"""목록에서 하나 선택하기"""
#getSelectInList함수에서 생성한 GUI의 버튼을 누르면 발동되는 함수.
def returnSelect(r):
    global encording_pop;
    global input_value;
    input_value = r;
    encording_pop.destroy();

#파일을 불러오는데 주로 사용함.
#list를 받아오면, 리스트에 있는 값 중 하나를 선택할 수 있는 팝업창을 생성하고, 하나를 선택했다면 선택한 값을 반환한다.
#X표를 눌러 창을 닫으면 None이 반환된다. 이 경우, 파일이 불러와지지 않는다.
def getSelectInList(list, win):
    global encording_pop;
    global input_value;
    input_value = None;
    encording_pop = tkinter.Toplevel();
    encording_pop.title("파일 불러오기");
    encording_pop.geometry("300x"+str(30*len(list)));
    a = 0;
    for file in list:
        button = tkinter.Button(encording_pop, text = file, command=lambda r=file:returnSelect(r));
        button.place(x=0, y=30*a, width = 300, height=30);
        a=a+1;
    win.wait_window(encording_pop);
    return input_value;
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
win = tkinter.Tk();

fileSave = None;
fileLoad = None;
option = None;

recordStart = None;
runStart = None;
reapeatStart = None;

isData = False;
programmode = 0 #[정지, 녹화, 시작, 반복시작, 저장, 불러오기, 인코딩, 옵션]

def clickFileSave():
    print("clickFileSave");

def clickFileLoad():
    print("clickFileLoad");

def clickOption():
    print("clickOption");

def clickRecordStart():
    print("clickRecordStart");

def clickStopRecord():
    print("clickStopRecord");

def clickRunStart():
    print("clickRunStart");

def clickStopRun():
    print("clickStopRun");

def clickReapeatStart():
    print("clickReapeatStart");

def clickStopReapeat():
    print("clickStopReapeat");

def replaceRecord(b):
    if(b):
        recordStart['text'] = "녹화시작";
        recordStart['command'] = clickRecordStart;
    else:
        recordStart['text'] = "녹화종료";
        recordStart['command'] = clickStopRecord;

def replaceRunStart(b):
    if(b):
        runStart['text'] = "시작";
        runStart['command'] = clickRunStart;
    else:
        runStart['text'] = "시작종료"
        runStart['command'] = clickStopRun;

def replaceReapeatStart(b):
    if(b):
        reapeatStart['text'] = "반복시작";
        reapeatStart['command'] = clickReapeatStart;
    else:
        reapeatStart['text'] = "반복종료"
        reapeatStart['command'] = clickStopReapeat;

def updateWindow():
    global fileSave;
    global fileLoad;
    global option;
    global recordStart;
    global runStart;
    global reapeatStart;
    match(programmode):
        case 0: #정지
            fileSave['state'] = tkinter.NORMAL;
            fileLoad['state'] = tkinter.NORMAL;
            option['state'] = tkinter.NORMAL;
            recordStart['state'] = tkinter.NORMAL;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
            if(isData):
                runStart['state'] = tkinter.NORMAL;
                reapeatStart['state'] = tkinter.NORMAL;
            else:
                runStart['state'] = tkinter.DISABLED;
                reapeatStart['state'] = tkinter.DISABLED;
        case 1: #녹화
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.NORMAL;
            runStart['state'] = tkinter.DISABLED;
            reapeatStart['state'] = tkinter.DISABLED;
            replaceRecord(0);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 2: #시작
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.DISABLED;
            runStart['state'] = tkinter.NORMAL;
            reapeatStart['state'] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(0);
            replaceReapeatStart(1);
        case 3: #반복시작
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.DISABLED;
            runStart['state'] = tkinter.DISABLED;
            reapeatStart['state'] = tkinter.NORMAL;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(0);
        case 4: #저장
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.DISABLED;
            runStart['state'] = tkinter.DISABLED;
            reapeatStart['state'] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 5: #불러오기
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.DISABLED;
            runStart['state'] = tkinter.DISABLED;
            reapeatStart['state'] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 6: #인코딩
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.DISABLED;
            runStart['state'] = tkinter.DISABLED;
            reapeatStart['state'] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 7: #옵션
            fileSave['state'] = tkinter.DISABLED;
            fileLoad['state'] = tkinter.DISABLED;
            option['state'] = tkinter.DISABLED;
            recordStart['state'] = tkinter.DISABLED;
            runStart['state'] = tkinter.DISABLED;
            reapeatStart['state'] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);


def initWindow():
    global win;
    global fileSave;
    global fileLoad;
    global option;
    global recordStart;
    global runStart;
    global reapeatStart;
    win.title("매크로");
    win.geometry("300x155+100+100");
    win.resizable(False, False);
    fileSave = tkinter.Button(win, text="저장", command=clickFileSave);
    fileSave.place(x=0, y=0, width=100, height=30);
    fileLoad = tkinter.Button(win, text="불러오기", command=clickFileLoad);
    fileLoad.place(x=100, y=0, width=100, height=30);
    option = tkinter.Button(win, text="설정", command=clickOption);
    option.place(x=200, y=0, width=100, height=30);
    recordStart = tkinter.Button(win, text="녹화", command=clickRecordStart);
    recordStart.place(x=0, y=60, width=100, height=95);
    runStart = tkinter.Button(win, text="시작", command=clickRunStart);
    runStart.place(x=100, y=60, width=100, height=95);
    reapeatStart = tkinter.Button(win, text="반복시작", command=clickReapeatStart);
    reapeatStart.place(x=200, y=60, width = 100, height=95);

    

"""초기화 시작"""
initWindow();
updateWindow();

"""프로그램 동작"""
with ml(on_click=on_click, on_scroll=on_scroll) as listener:
    with kl(on_press=on_press, on_release=on_release) as listener:
        win.mainloop();

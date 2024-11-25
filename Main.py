import tkinter;
from pynput.keyboard import Listener as kl;
from pynput.mouse import Listener as ml;
from api import Record, Runner, configSaver;
import threading;
import pynput;

"""PROGRAM이벤트들"""
programmode = 0 #[정지, 녹화, 시작, 반복시작, 저장, 불러오기, 인코딩, 옵션]

#단축키 정리
hotkeys = {"recordStart":pynput.keyboard.Key.f9,
           "recordStop":pynput.keyboard.Key.f9,
           "startRun":pynput.keyboard.Key.f10,
           "stopRun":pynput.keyboard.Key.f10,
           "repeatRun":pynput.keyboard.Key.f11,
           "stoprRun":pynput.keyboard.Key.f11};

#각 키에 무슨 이벤트들이 있는지 모두 정리
keydata = {};

#이벤트 실행, 실행 불가능하면 0을 반환
def actionEvent(name):
    global recordStart;
    global runStart;
    global reapeatStart;
    global programmode;
    match(name):
        case "recordStart":
            if(recordStart["state"]==tkinter.NORMAL and programmode==0):
                recordStart.invoke();
                return 1;
        case "recordStop":
            if(recordStart["state"]==tkinter.NORMAL and programmode==1):
                recordStart.invoke();
                return 1;
        case "startRun":
            if(runStart["state"]==tkinter.NORMAL and programmode==0):
                runStart.invoke();
                return 1;
        case "stopRun":
            if(runStart["state"]==tkinter.NORMAL and programmode==2):
                runStart.invoke();
                return 1;
        case "repeatRun":
            if(reapeatStart["state"]==tkinter.NORMAL and programmode==0):
                reapeatStart.invoke();
                return 1;
        case "stoprRun":
            if(reapeatStart["state"]==tkinter.NORMAL and programmode==3):
                reapeatStart.invoke();
                return 1;
    return 0;

#Key에 해당하는 이벤트를 실행(하나만)
#실행이 되지 않으면 0을 반환
def runHotKey(Key):
    global keydata;
    if Key in keydata:
        for act in keydata[Key].split(","):
            if(actionEvent(act)):
                return 1;
    return 0;

#하나의 Keydata를 생성
def loadKey(active, key):
    global keydata;
    if key in keydata:
        keydata[key] = keydata[key]+","+active;
    else:
        keydata[key] = active;

#keydata를 초기화함
def clearAllKey():
    global keydata;
    keydata = {};

#hotkeys데이터를 바탕으로 모든 keydata를 생성
def initAllKey():
    clearAllKey();
    global hotkeys;
    for key in hotkeys:
        loadKey(key, hotkeys[key]);

#사용자지정파일을 로드함
def loadOption():
    configSaver.load();

#사용자지정파일을 저장함
def saveOption():
    configSaver.save();

#반복을 시작함
def startRun(dic):
    Runner.start(dic);

#반복을 종료함
def repeatRun(dic):
    Runner.repeatStart(dic);

"""입력 이벤트들"""
#마우스 클릭 이벤트
def on_click(x, y, button, pressed):
    print(x, y, button, pressed);
    if(programmode==1):
        Record.add_input(("click", x, y, button, pressed));

#마우스 스크롤 이벤트
def on_scroll(x, y, dx, dy):
    print(x, y, dx, dy);
    if(programmode==1):
        Record.add_input(("scroll", x, y, dx, dy));

#키보드 다운 이벤트
def on_press(key):
    print(key, "press");
    if(runHotKey(key)):
        return;
    if(programmode==1):
        Record.add_input(("press", key));


#키보드 업 이벤트
def on_release(key):
    print(key, "release");
    if(programmode==1):
        Record.add_input(("release", key));

"""GUI이벤트들"""
win = tkinter.Tk();

fileSave = None;
fileLoad = None;
option = None;

recordStart = None;
runStart = None;
reapeatStart = None;

isData = False;

def updateWindow():
    global fileSave;
    global fileLoad;
    global option;
    global recordStart;
    global runStart;
    global reapeatStart;
    global programmode;
    global isData;
    match(programmode):
        case 0: #정지
            fileSave["state"] = tkinter.NORMAL;
            fileLoad["state"] = tkinter.NORMAL;
            option["state"] = tkinter.NORMAL;
            recordStart["state"] = tkinter.NORMAL;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
            if(isData):
                runStart["state"] = tkinter.NORMAL;
                reapeatStart["state"] = tkinter.NORMAL;
            else:
                runStart["state"] = tkinter.DISABLED;
                reapeatStart["state"] = tkinter.DISABLED;
            return;
        case 1: #녹화
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.NORMAL;
            runStart["state"] = tkinter.DISABLED;
            reapeatStart["state"] = tkinter.DISABLED;
            replaceRecord(0);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 2: #시작
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.DISABLED;
            runStart["state"] = tkinter.NORMAL;
            reapeatStart["state"] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(0);
            replaceReapeatStart(1);
        case 3: #반복시작
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.DISABLED;
            runStart["state"] = tkinter.DISABLED;
            reapeatStart["state"] = tkinter.NORMAL;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(0);
        case 4: #저장
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.DISABLED;
            runStart["state"] = tkinter.DISABLED;
            reapeatStart["state"] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 5: #불러오기
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.DISABLED;
            runStart["state"] = tkinter.DISABLED;
            reapeatStart["state"] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 6: #인코딩
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.DISABLED;
            runStart["state"] = tkinter.DISABLED;
            reapeatStart["state"] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
        case 7: #옵션
            fileSave["state"] = tkinter.DISABLED;
            fileLoad["state"] = tkinter.DISABLED;
            option["state"] = tkinter.DISABLED;
            recordStart["state"] = tkinter.DISABLED;
            runStart["state"] = tkinter.DISABLED;
            reapeatStart["state"] = tkinter.DISABLED;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);

def clickFileSave():
    global programmode;
    print("clickFileSave");

def clickFileLoad():
    global programmode;
    global isData;
    isData = True;
    updateWindow();
    print("clickFileLoad");

def clickOption():
    global programmode;
    print("clickOption");

def clickRecordStart():
    global programmode;
    programmode = 1;
    updateWindow();
    Record.start();
    print("clickRecordStart");

def clickStopRecord():
    global programmode;
    global isData;
    programmode = 0;
    isData = True;
    updateWindow();
    Record.stop();
    print("clickStopRecord");

def clickRunStart():
    global programmode;
    programmode = 2;
    updateWindow();
    threading.Thread(target=startRun, args=(Record.getSaves()));
    print("clickRunStart");

def clickStopRun():
    global programmode;
    programmode = 0;
    updateWindow();
    Runner.stop();
    print("clickStopRun");

def clickReapeatStart():
    global programmode;
    programmode = 3;
    updateWindow();
    threading.Thread(target=repeatRun, args=(Record.getSaves()));
    print("clickReapeatStart");

def clickStopReapeat():
    global programmode;
    programmode = 0;
    updateWindow();
    Runner.stop();
    print("clickStopReapeat");

def replaceRecord(b):
    global recordStart;
    if(b):
        recordStart['text'] = "녹화시작";
        recordStart['command'] = clickRecordStart;
    else:
        recordStart['text'] = "녹화종료";
        recordStart['command'] = clickStopRecord;

def replaceRunStart(b):
    global runStart;
    if(b):
        runStart['text'] = "시작";
        runStart['command'] = clickRunStart;
    else:
        runStart['text'] = "시작종료"
        runStart['command'] = clickStopRun;

def replaceReapeatStart(b):
    global repeatStart;
    if(b):
        reapeatStart['text'] = "반복시작";
        reapeatStart['command'] = clickReapeatStart;
    else:
        reapeatStart['text'] = "반복종료"
        reapeatStart['command'] = clickStopReapeat;

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
loadOption();
initAllKey();
print(keydata);

"""프로그램 동작"""
with ml(on_click=on_click, on_scroll=on_scroll) as listener:
    with kl(on_press=on_press, on_release=on_release) as listener:
        win.mainloop();
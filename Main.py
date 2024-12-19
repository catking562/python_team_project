import tkinter #gui 생성 모듈
import tkinter.messagebox; #메시지박스 생성 모듈
from pynput.keyboard import Listener as kl; #키보드 키 입력 감지
from pynput.mouse import Listener as ml; # 마우스 키 입력 감지
import threading; #파이썬 파일의 동시 접근을 위한 모듈
import pynput;  
import time;
from api import Record, Runner, configSaver, FileSaver, CreatePoP, DataEncoder; #api 폴더에서 각 파일들을 임포트

"""버그방지용"""

"""PROGRAM이벤트들"""
programmode = 0 #[정지, 녹화, 시작, 반복시작, 저장, 불러오기, 인코딩, 옵션]

#단축키 정리 (초기화된 단축키)
hotkeys = {"recordStart":"Key.f9", #녹화시작: f9
           "recordStop":"Key.f9", #녹화멈춤 : f9
           "startRun":"Key.f10",  #시작: f10
           "stopRun":"Key.f10", #종료: f10
           "repeatRun":"Key.f11", #반복: f11
           "stoprRun":"Key.f11"}; #반복종료: f11

#각 키에 무슨 이벤트들이 있는지 모두 정리
keydata = {}; 

#이벤트 실행, 실행 불가능하면 0을 반환
def actionEvent(name): 
    global recordStart; 
    global runStart;
    global reapeatStart;
    global programmode;
    match(name):  #각 이벤트가 들어오면 해당하는 코드를 실행함.
        case "recordStart":
            if(recordStart["state"]==tkinter.NORMAL and programmode==0):
                recordStart.invoke(); #버튼을 클릭함.
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
    if str(Key) in keydata:
        for act in keydata[str(Key)].split(","):  #','를 구분자로 배열되어 있는 것을 분리하고, 각 이벤트 실행 (하나라도 실행성공하면 return 1)
            if(actionEvent(act)):
                return 1;
    return 0;

#하나의 Keydata를 생성
def loadKey(active, key):
    global keydata;
    if key in keydata:
        keydata[key] = keydata[key]+","+active;  #비슷한 단축키가 있는 경우, ','를 구분자로 해서 저장함.
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
        loadKey(key, hotkeys[key]);  #<key, value>를 <value, key>의 형태로 바꿈

#사용자지정파일을 로드함
def loadOption():
    global hotkeys;
    configSaver.load();  #option.txt파일을 로드함.
    for hotkey in hotkeys:
        if not configSaver.isKey(hotkey):  #option.txt에 값이 없다면 초기 값을 지정해줌
            configSaver.put(hotkey, hotkeys[hotkey]);
    for hotkey in configSaver.get_All():   #마지막으로 option.txt파일 전체를 hotkeys에 반영해줌.
        hotkeys[hotkey] = configSaver.get(hotkey);

#사용자지정파일을 저장함
def saveOption():
    global hotkeys;
    for hotkey in hotkeys:
        configSaver.put(hotkey, str(hotkeys[hotkey]));  #hotkeys에 있는 데이터를 option.txt에 저장
    configSaver.save();

"""입력 이벤트들"""
#마우스 클릭 이벤트
def on_click(x, y, button, pressed):
    print(x, y, button, pressed);
    if(programmode==1):                                                           #녹화중인지 확인
        Record.add_input([time.perf_counter(), "click", x, y, button, pressed]);  #Record에 데이터를 보냄

#마우스 스크롤 이벤트
def on_scroll(x, y, dx, dy):
    print(x, y, dx, dy);
    if(programmode==1):                                                     #녹화중인지 확인
        Record.add_input([time.perf_counter(), "scroll", x, y, dx, dy]);    #Record에 데이터를 보냄

#키보드 다운 이벤트
def on_press(key):
    print(key, "press");
    if(runHotKey(key)):
        return;
    if(programmode==1):                                              #녹화중인지 확인
        Record.add_input([time.perf_counter(), "press", key]);       #Record에 데이터를 보냄
        return;
    if(programmode==7 and CreatePoP.isneedButton()):       #설정에서 키 변경중인지 확인
        CreatePoP.setButton(key);                          #CreatePoP에 키 데이터를 보내줌
        CreatePoP.closeMiniPop();                          #키 설정 창을 닫음. (이후 hotkeys에 저장됨)


#키보드 업 이벤트
def on_release(key):
    print(key, "release");
    if(programmode==1):                                             #녹화중인지 확인
        Record.add_input([time.perf_counter(), "release", key]);    #Record에 데이터를 보냄

"""GUI이벤트들"""
win = tkinter.Tk();

fileSave = None;
fileLoad = None;
option = None;

recordStart = None;
runStart = None;
reapeatStart = None;

isData = False;
recordData = None;

#GUI를 업데이트 함.
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
            fileLoad["state"] = tkinter.NORMAL;  #버튼 활성화
            option["state"] = tkinter.NORMAL;
            recordStart["state"] = tkinter.NORMAL;
            replaceRecord(1);
            replaceRunStart(1);
            replaceReapeatStart(1);
            if(isData):
                runStart["state"] = tkinter.NORMAL;
                reapeatStart["state"] = tkinter.NORMAL;
                fileSave["state"] = tkinter.NORMAL;
            else:
                runStart["state"] = tkinter.DISABLED;  #버튼 비활성화
                reapeatStart["state"] = tkinter.DISABLED;
                fileSave["state"] = tkinter.DISABLED;
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

#저장 버튼을 클릭했을 때 실행
def clickFileSave():
    global win;
    global programmode;
    programmode = 4;
    updateWindow();
    #파일이름 물어보는 팝업
    name = CreatePoP.getFileName(win);
    #저장 중 팝업
    CreatePoP.createMessage("저장 중...");
    #저장 시작
    if(name!=None):
        FileSaver.saveFile(DataEncoder.encoding_Tostr(recordData), name);
    #저장 끝
    CreatePoP.destroy();
    programmode = 0;
    updateWindow();
    print("clickFileSave");

#로드 버튼을 클릭했을 때 실행
def clickFileLoad():
    global programmode;
    global isData;
    global recordData;
    programmode = 5;
    updateWindow();
    sel = CreatePoP.getSelectInList(FileSaver.getSavedFileNames(), win);
    if(sel!=None):
        recordData = DataEncoder.encoding_bystr(FileSaver.loadFile(sel));
        isData = True;
    programmode = 0;
    updateWindow();
    print("clickFileLoad");

#설정버튼을 클릭했을 때 실행
def clickOption():
    global programmode;
    global hotkeys;
    global win;
    programmode = 7;
    updateWindow();
    CreatePoP.editOption(hotkeys, win);
    initAllKey();
    saveOption();
    programmode = 0;
    updateWindow();
    print("clickOption");

#녹화버튼을 클릭했을 때 실행
def clickRecordStart():
    global programmode;
    programmode = 1;
    updateWindow();
    Record.start();
    print("clickRecordStart");

#녹화종료 버튼을 클릭했을 때 실행
def clickStopRecord():
    global programmode;
    global isData;
    global recordData;
    #녹화종료
    isData = True;
    programmode = 6;
    updateWindow();
    Record.stop();
    #인코딩
    CreatePoP.createMessage("인코딩 중...");
    recordData = DataEncoder.encoding_Torun(Record.get_save());
    #인코딩 완료
    CreatePoP.destroy();
    programmode = 0;
    updateWindow();
    print("clickStopRecord");

#시작 버튼을 클릭했을 때 실행
def clickRunStart():
    global programmode;
    global recordData;

    #반복을 시작함
    def startRun(dic):
        Runner.start(dic);

    programmode = 2;
    updateWindow();
    task = threading.Thread(target=startRun, args=(recordData,));
    task.start();
    print("clickRunStart");

#종료 버튼을 클릭했을 때 실행
def clickStopRun():
    global programmode;
    programmode = 0;
    updateWindow();
    Runner.stop();
    print("clickStopRun");

#반복시작 버튼을 클릭했을 때 실행
def clickReapeatStart():
    global programmode;
    global recordData;

    #반복을 종료함
    def repeatRun(dic):
        Runner.repeatStart(dic);

    programmode = 3;
    updateWindow();
    task = threading.Thread(target=repeatRun, args=(recordData,));
    task.start();
    print("clickReapeatStart");

#반복종료 버튼을 클릭했을 때 실행
def clickStopReapeat():
    global programmode;
    programmode = 0;
    updateWindow();
    Runner.stop();
    print("clickStopReapeat");

#녹화 버튼을 녹화종료로 바꾸는 용도. (반대도 마찬가지)
def replaceRecord(b):
    global recordStart;
    if(b):
        recordStart['text'] = "녹화시작";
        recordStart['command'] = clickRecordStart;
    else:
        recordStart['text'] = "녹화종료";
        recordStart['command'] = clickStopRecord;

#시작 버튼을 시작종료로 바꾸는 용도. (반대도 마찬가지)
def replaceRunStart(b):
    global runStart;
    if(b):
        runStart['text'] = "시작";
        runStart['command'] = clickRunStart;
    else:
        runStart['text'] = "시작종료"
        runStart['command'] = clickStopRun;

#반복시작 버튼을 반복종료로 바꾸는 용도. (반대도 마찬가지)
def replaceReapeatStart(b):
    global repeatStart;
    if(b):
        reapeatStart['text'] = "반복시작";
        reapeatStart['command'] = clickReapeatStart;
    else:
        reapeatStart['text'] = "반복종료"
        reapeatStart['command'] = clickStopReapeat;

#윈도우를 초기화함. (버튼을 생성하고, 변수의 초기값을 정하는 과정이 포함됨.)
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

"""프로그램 동작"""
with ml(on_click=on_click, on_scroll=on_scroll) as listener:
    with kl(on_press=on_press, on_release=on_release) as listener:
        win.mainloop();

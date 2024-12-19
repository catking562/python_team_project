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
programmode = 0 #[0: 정지, 1:녹화, 2:시작, 3:반복시작, 4:저장, 5:불러오기, 6:인코딩, 7:옵션]

#단축키 정리 (초기화된 단축키)
hotkeys = {"recordStart":"Key.f9", #녹화시작: f9
           "recordStop":"Key.f9", #녹화멈춤 : f9
           "startRun":"Key.f10",  #시작: f10
           "stopRun":"Key.f10", #종료: f10
           "repeatRun":"Key.f11", #반복: f11
           "stoprRun":"Key.f11"}; #반복종료: f11

#특정 이벤트를 발생하는 키와 그에 해당하는 이벤트를 딕셔너리 형태로 저장
"""
ex) keydata = {"Key.f9":"recordStart", "recordStop", ...}
f9를 누르면 recordStart 혹은 recordStop에 해당하는 이벤트를 발생하므로 위와 같은 형태로 딕셔너리에 저장
이렇게 저장된 keydata는 actionEvent를 통하여 단축키 이벤트를 수행.
"""
keydata = {}; 

#이벤트 실행, 실행 불가능하면 0을 반환
#단축키를 누르면 발생되고, 변수는 누른 단축키와 매칭되어 있는 이름을 변수로 사용
def actionEvent(name): 
    global recordStart;  #녹화 버튼 참조
    global runStart; #실행 버튼 참조
    global reapeatStart; #반복 실행 버튼 참조
    global programmode; #현재 프로그램 상태 참조

    # (버튼함수).invoke() => 해당 버튼이 눌려지는 처리
    # 어떤 버튼이 눌리면 다른 버튼이 활성화/비활성화가 되며, 시작 버튼 <-> 종료 버튼 상태가 바뀜.      
    match(name):  #누른 단축키에 따른 이벤트 활성화
        case "recordStart": #녹화 시작 단축키를 누르면 발생하는 이벤트
            if(recordStart["state"]==tkinter.NORMAL and programmode==0): #조건: 녹화 버튼이 활성화 된 상태이고, 프로그램 모드가 정지 상태
                recordStart.invoke(); #녹화 시작 버튼이 눌림
                return 1;
        case "recordStop": #녹화 중지 단축키를 누르면 발생하는 이벤트
            if(recordStart["state"]==tkinter.NORMAL and programmode==1): #조건 : 녹화 종료 버튼(녹화 버튼이었던 것)이 활성화 상태이고, 프로그램 모드가 녹화 상태
                recordStart.invoke(); #녹화 종료 버튼이 눌림
                return 1;
        case "startRun": #시작 단축키를 누르면 발생하는 이벤트
            if(runStart["state"]==tkinter.NORMAL and programmode==0): #조건: 시작 버튼이 활성화 되어있고, 프로그램 모드가 정지 상태
                runStart.invoke(); #시작 버튼이 눌림
                return 1;
        case "stopRun": #시작 종료 단축키를 누르면 발생하는 이벤트
            if(runStart["state"]==tkinter.NORMAL and programmode==2): #조건: 시작 종료 버튼(시작 버튼이었던 것)이 활성화 상태이고, 프로그램 모드가 시작 상태
                runStart.invoke(); #시작 종료 버튼이 눌림
                return 1;
        case "repeatRun": #반복 시작 단축키를 누르면 발생하는 이벤트
            if(reapeatStart["state"]==tkinter.NORMAL and programmode==0): #조건: 반복 시작 버튼이 활성화 상태, 프로그램 모드가 정지 상태
                reapeatStart.invoke(); #반복 시작 버튼이 눌림
                return 1;
        case "stoprRun": #반복 중지 단축키를 누르면 발생하는 이벤트
            if(reapeatStart["state"]==tkinter.NORMAL and programmode==3): #조건: 반복 중지 버튼(반복 시작 버튼이었던 것)이 활성화 상태, 프로그램 모드가 반복 실행 상태
                reapeatStart.invoke(); #반복 종료 버튼이 눌림.
                return 1;
    return 0; #이벤트 실행 불가 시 0을 반환

#키보드 인식 함수를 통해서 키가 눌릴 때마다 단축키인지 확인 및 단축키에 해당하는 함수를 실행
#실행이 되지 않으면 0을 반환
def runHotKey(Key):
    global keydata;
    if str(Key) in keydata: #입력된 키보드의 키가 keydata 딕셔너리에서 존재하는지 확인(단축키인지 확인하는 if문)
        for act in keydata[str(Key)].split(","):  #keydate에서 이벤트를 for문의 인자로 넣음
            if(actionEvent(act)): #해당 함수 내에서 조건에 따라 단축키 실행
                return 1;
    return 0;

#하나의 Keydata를 생성
def loadKey(active, key):
     #특정 키에 이벤트를 연결 . 같은 키에 여러 이벤트가 연결될 경우 ','로 구분해 저장
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
    #hokeys딕셔너리를 기반으로 keydata를 초기화
    clearAllKey();
    global hotkeys;
    for key in hotkeys:
        loadKey(key, hotkeys[key]);  #<key, value>를 <value, key>의 형태로 바꿈

#사용자지정파일을 로드함
def loadOption():
    #사용자 설정 파일을 로드하고 , hotkeys에 반영
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
    #마우스 클릭 이벤트 발생 시 실행. 녹화 중일 경우 해당 데이터를 Record에 저장
    print(x, y, button, pressed);
    if(programmode==1):                                                           #녹화중인지 확인
        Record.add_input([time.perf_counter(), "click", x, y, button, pressed]);  #Record에 데이터를 보냄

#마우스 스크롤 이벤트
def on_scroll(x, y, dx, dy):
    #마찬가지로 마우스 스크롤 이벤트 발생 시.
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

    #GUI버튼을 통해서 변경된 프로그램모드에 따라 GUI버튼을 비활성화시키거나 활성화시킨다.       
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
    global win; #창 객체
    global programmode; #현재 프로그램 상태를 나타내는 전역 변수
    programmode = 4; #프로그램 상태를 '저장'으로 설정
    updateWindow(); #GUI 버튼 상태를 업데이트
    #파일이름 물어보는 팝업
    name = CreatePoP.getFileName(win); #저장할 파일 이름을 사용자에게 입력받는 팝업 창 호출
    #저장 중 이라는 메시지를 표시하는 팝업 창 생성
    CreatePoP.createMessage("저장 중...");
    #파일 이름이 입력된 경우 데이터를 파일로 저장
    if(name!=None):
        FileSaver.saveFile(DataEncoder.encoding_Tostr(recordData), name);
    #저장 끝
    CreatePoP.destroy();
    programmode = 0;
    updateWindow();
    print("clickFileSave");

#로드 버튼을 클릭했을 때 실행
def clickFileLoad():
    global programmode; #프로그램 상태 전역 변수
    global isData; #데이터가 있는지 여부를 나타내는 전역 변수
    global recordData; #녹화된 데이터를 저장하는 전역 변수
    programmode = 5; #프로그램 상태를 '불러오기'로 설정
    updateWindow(); #GUI버튼 상태를 업데이트
    #저장된 파일 목록을 사용자에게 사용자에게 보여주고 선택하도록 팝업 생성
    sel = CreatePoP.getSelectInList(FileSaver.getSavedFileNames(), win);
    if(sel!=None): #사용자가 파일을 선택한 경우, 데이터를 로드하고 recordData에 저장
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
    programmode = 7; #프로그램 상태를 '설정'으로 변경
    updateWindow(); #gui업데이트
    CreatePoP.editOption(hotkeys, win); #사용자 설정을 편집할 수 있는 팝업 창 호출
    initAllKey(); #단축키 설정을 새로 고침
    saveOption(); #새로운 단축키 설정을 저장
    programmode = 0; #프로그램 상태를 '정지'로 변경
    updateWindow();
    print("clickOption");

#녹화버튼을 클릭했을 때 실행
def clickRecordStart(): 
    global programmode; 
    programmode = 1; #프로그램 상태를 '녹화'로 변경
    updateWindow();
    Record.start(); #Record.py에서 start() 함수 실행
    print("clickRecordStart");

#녹화종료 버튼을 클릭했을 때 실행
def clickStopRecord(): 
    global programmode;
    global isData; #데이터가 있는지 여부를 나타내는 전역 변수
    global recordData; #녹화된 데이터를 저장하는 전역변수
    #녹화종료
    isData = True; #데이터를 성공적으로 녹화했음을 표시
    programmode = 6; #프로그램 상태를 '인코딩'으로 변경
    updateWindow();
    Record.stop(); #Record.py에서 stop()함수 실행
    #인코딩
    CreatePoP.createMessage("인코딩 중..."); #인코딩 중... 이라는 메시지를 표시하는 팝업 창 생성
    recordData = DataEncoder.encoding_Torun(Record.get_save()); #녹화 데이터를 실행 가능한 현태로 인코딩하여 recordData에 저장
    #인코딩 완료 후 팝업 창 제거
    CreatePoP.destroy();
    programmode = 0;
    updateWindow();
    print("clickStopRecord");

#실행 버튼 클릭 시 실행되는 함수
def clickRunStart():
    global programmode; #프로그램 상태 전역 변수
    global recordData; #실행할 데이터

    #반복을 시작함
    def startRun(dic): #데이터를 실행하는 함수 정의(쓰레드에서 실행될 함수)
        Runner.start(dic); #Runner.py 에서 start()함수 실행

    programmode = 2; #프로그램 상태를 '실행'으로 변경
    updateWindow(); 
    task = threading.Thread(target=startRun, args=(recordData,)); #실행 작업을 별도 쓰레드에서 처리
    task.start(); #쓰레드에서 부른 함수와 데이터를 이용하여 시작
    print("clickRunStart");

#종료 버튼을 클릭했을 때 실행
def clickStopRun():
    global programmode;
    programmode = 0; #프로그램 상태를 '정지'로 변경
    updateWindow();
    Runner.stop();
    print("clickStopRun");

#반복시작 버튼을 클릭했을 때 실행
def clickReapeatStart():
    global programmode;
    global recordData; #반복 실행할 데이터

    #반복을 종료함
    def repeatRun(dic): #반복 실행 작업을 처리하는 함수 정의(쓰레드에서 실행될 함수)
        Runner.repeatStart(dic); #Runner에서 repeatStart함수 실행

    programmode = 3; #프로그램 상태를 '반복 실행'으로 변경
    updateWindow();
    task = threading.Thread(target=repeatRun, args=(recordData,)); #반복 실행 작업을 별도 쓰레드에서 처리
    task.start();
    print("clickReapeatStart");

#반복종료 버튼을 클릭했을 때 실행
def clickStopReapeat(): 
    global programmode;
    programmode = 0; #프로그램 상태를 정지로 변경
    updateWindow();
    Runner.stop(); #반복 실행 작업 종료 (Runner 에서 stop실행)
    print("clickStopReapeat");

#녹화 버튼을 녹화종료로 바꾸는 용도. (반대도 마찬가지)
def replaceRecord(b):
    global recordStart; #녹화 버튼 객체
    if(b): #녹화 시작 상태로 변경
        recordStart['text'] = "녹화시작";
        recordStart['command'] = clickRecordStart;
    else:
        recordStart['text'] = "녹화종료";
        recordStart['command'] = clickStopRecord;

#시작 버튼을 시작종료로 바꾸는 용도. (반대도 마찬가지)
def replaceRunStart(b):
    global runStart; #실행 버튼 객체
    if(b): #실행 시작 상태로 변경
        runStart['text'] = "시작";
        runStart['command'] = clickRunStart;
    else:
        runStart['text'] = "시작종료"
        runStart['command'] = clickStopRun;

#반복시작 버튼을 반복종료로 바꾸는 용도. (반대도 마찬가지)
def replaceReapeatStart(b):
    global repeatStart; #반복 실행 버튼 객체
    if(b): #반복 실행 상태로 변경
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
initWindow(); #GUI창을 초기화. 버튼 생성 및 배치, 변수 초기화
updateWindow(); #초기 상태에 맞춰 gui업데이트. 버튼 상태 및 텍스트 초기화
loadOption(); #사용자 설정 파일을 불러와 단축키 등의 설정을 초기화
initAllKey(); #단축키 데이터를 기반으로 키 이벤트를 매핑

"""프로그램 동작"""
#마우스 및 키보드 listner을 실행하면서 tkinter gui메인 루프를 함께 운영
#listner는 마우스 및 키보드 입력 이벤트를 감지, 처리 , gui는 사용자 인터페이스 관리
with ml(on_click=on_click, on_scroll=on_scroll) as listener: #마우스 listner실행
           #on_click: 마우스 클릭 이벤트 처리  , on_scroll: 마우스 스크롤 이벤트 처리
    with kl(on_press=on_press, on_release=on_release) as listener: #키보드 리스너 실행
           #on_press: 키가 눌렸을 때 호출 , #on_realease: 키가 해제되었을 때 호출
        win.mainloop();
           #tkinter GUI메인 루프 실행
           #mainloop는 GUI이벤트 루프를 유지하며 사용자가 창을 클릭하는 등의 이벤트로 처리

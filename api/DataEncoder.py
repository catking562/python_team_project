import pynput;
from pynput.keyboard import Key

# Key 클래스의 __repr__을 재정의
def custom_repr(self):
    return f"{self}"

# Key 클래스의 __repr__ 메서드 변경
Key.__repr__ = custom_repr

#단축키 딕셔너리를 넣으면 문자열 형태로 변경됨.
#주의 : 그대로 파일에 써넣기만 할 것
def encode_save_hotkeys(hotkeys):
    str_hotkeys = repr(hotkeys)
    return str_hotkeys

#단축키 문자열을 딕셔너리로 바꿈.
#사용 방법 : hotkeys = encode_load_hotkeys(str_hotkeys) 형태로 사용
def encode_load_hotkeys(str_hotkeys):
    return eval(str_hotkeys)

def encoding_Torun(control):
    control = sorted(control, key = lambda x:x[0])
    if len(control)==0:
        return control;
    startTime = control[0][0]
    
    for i in range(len(control)) :
        control[i][0] = control[i][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.
        startTime = startTime + control[i][0];
        
        if control[i][1] == "click":
            if control[i][5] ==True:
                start_x, start_y = control[i][2], control[i][3]
            else:
                print(control[i])
                turm_x, turm_y = control[i][2] - start_x, control[i][3] - start_y
                control[i].append(turm_x)
                control[i].append(turm_x)

    return control;

def encoding_Tostr(control):
    control_str = repr(control)
    return control_str

def encoding_bystr(save_string):
    control = eval(save_string)
    return control

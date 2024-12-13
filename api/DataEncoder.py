import pynput;

#단축키 딕셔너리를 넣으면 문자열 형태로 변경됨.
#주의 : 그대로 파일에 써넣기만 할 것
def encode_save_hotkeys(hotkeys):
    temp_dic = {}

    for key, value in hotkeys.items():
        str_value = str(value)
        temp_dic[key] = "pynput.keybord." + str_value
    
    str_hotkeys = repr(temp_dic)
    return str_hotkeys

#단축키 문자열을 딕셔너리로 바꿈.
#사용 방법 : hotkeys = encode_load_hotkeys(str_hotkeys) 형태로 사용
def encode_load_hotkeys(str_hotkeys):
    
    return eval(str_hotkeys)
    
def encoding_Torun(control):
    control = sorted(control, key = lambda x:x[0])
    startTime = control[0][0]
    
    for i in range(len(control)) :
        control[i][0] = control[i][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.

    return control;

def encoding_Tostr(control):
    control_str = repr(control)
    return control_str

def encoding_bystr(save_string):
    control = eval(save_string)
    return control


import pynput;

# Key 클래스의 __repr__을 재정의
def custom_repr(self):
    return f"pynput.keyboard.{self}"

# Key 클래스의 __repr__ 메서드 변경
pynput.keyboard.Key.__repr__ = custom_repr

def encoding_Torun(control):
    control = sorted(control, key = lambda x:x[0])
    startTime = control[0][0]
    
    for i in range(len(control)) :
        control[i][0] = control[i][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.
        startTime = startTime + control[i][0];
    return control;

#파이썬 기본 자료형을 문자열로 변경
#추가로 불러온 매소드는 따로 __repr__를 변경해야함.
#pynput의 Key 클래스의 __repr__는 변경되었으므로 밑의 인코딩 함수만 사용하면 됨.

def encoding_Tostr(control):
    control_str = repr(control)
    return control_str

def encoding_bystr(save_string):
    control = eval(save_string)
    return control

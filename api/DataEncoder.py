import pynput;
from pynput.keyboard import Key

# Key 클래스의 __repr__을 재정의
def custom_repr(self):
    return f"{self}"  # Key 객체를 그대로 문자열로 표현


# Key 클래스의 __repr__ 메서드 변경
# Key 객체가 repr함수로 변환할 때, 문자열로 표시되는 방식을 사용자 정의
Key.__repr__ = custom_repr

#녹화를 통해 저장된 데이터를 가공하여 Runner로 넘기는 함수
def encoding_Torun(control):
    #데이터들을 시간순으로 정렬(controld의 형식: [[프로그램 시작으로부터의 시간, 동작...], ...])
    #lambda의 x는 control의 하위 리스트이므로 기준을 정하기 위해 x[0]로 sorted함수의 키를 설정.
    control = sorted(control, key = lambda x:x[0])
    
    #f9를 누른 후 임의의 조작 없이 바로 종료 시, 오류가 나지 않게 control을 반환
    if len(control)==0:
        return control;
    
    #출력을 위한 형식 : [[이전 출력 이벤트에서 시간 간격, 동작...], ...]
    #첫 출력 시작 시간을 기준으로 잡기
    startTime = control[0][0]
    
    #동작할 출력의 개수만큼 반복문 시행
    for i in range(len(control)) :
        #이전 출력 이벤트에서 시간 간격을 계산 후, control에 대입
        control[i][0] = control[i][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.
        startTime = startTime + control[i][0];

    return control;

#들어온 데이터를 문자열로 반환
def encoding_Tostr(control):
    #repr는 객체를 다시 생성할 수 있는 문자열 형태로 반환.(eval을 사용하면 다시 문자열 형태의 표현식을 실행)
    control_str = repr(control)
    return control_str

#들어온 문자열 형태의 동작 데이터를 리스트로 변환
def encoding_bystr(save_string):
    #repr를 통해 다시 생성 가능한 문자열 형태이므로 eval만 사용 시, 완
    control = eval(save_string)
    return control

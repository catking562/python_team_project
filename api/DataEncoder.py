def encoding(dictionary):
    encode = {};
    #dictionary데이터를 encode로 인코딩
    #데이터를 {<다음 동작까지 걸리는 시간>:<다음 동작>}
    #으로 변경
    return encode;

def encode(control):
    control = sorted(control, key = lambda x:x[0])
    startTime = control[0][0]

    for i in control :
        control[0][0] = control[0][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.

    return control;

def encode_str(control):
    

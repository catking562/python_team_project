
def encoding(control):
    control = sorted(control, key = lambda x:x[0])
    startTime = control[0][0]

    for i in control :
        control[0][0] = control[0][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.

    return control;

def encode_str(control):
    return control

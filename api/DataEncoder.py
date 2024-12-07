
def encoding_Torun(control):
    startTime = control[0];
    del control[0];
    print(control[0][0]);
    control = sorted(control, key = lambda x:x[0])

    for i in range(len(control)):
        control[i][0] = control[i][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.
        startTime+=control[i][0];
    return control;

def encoding_Tostr(control):
    control_str = repr(control)
    return control_str

def encoding_bystr(save_string):
    control = eval(save_string)
    return control


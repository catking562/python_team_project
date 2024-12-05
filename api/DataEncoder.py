
def encoding_Torun(control):
    control = sorted(control, key = lambda x:x[0])
    startTime = control[0][0]

    for i in range(len(control)) :
        control[i][0] = control[i][0] - startTime #시작 시간으로부터 행동 시간을 뺀 간격.

    return control;

def encoding_Tostr(control):
    for i in range(len(control)):
        control[i] = ','.join(control[i])

    control_str = '\n'.join(control)
    return control

def encoding_bystr(save_string):
    control = save_string.split('\n')
    
    for i in range(len(control)):
        control[i] = control[i].split(',')
        
    for i in range(len(control)):
        for j in range(len(control[j])):
            if (control[i][j].isdigit() == True):
                control[i][j] = int(control[i][j])
                
    return control


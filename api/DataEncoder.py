
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
            control[i][0] = int(control[i][0])
            
            if (control[i][1] == "scroll"):
                control[i][2] = int(control[i][2])
                control[i][3] = int(control[i][3])
                control[i][4] = int(control[i][4])
                control[i][5] = int(control[i][5])
            
            if (control[i][1] == "scroll"):
                control[i][2] = int(control[i][2])
                control[i][3] = int(control[i][3])
                
                
    return control


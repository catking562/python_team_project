re_control = ()
def encode_input(control):
    global re_control

    time = 0
    temp = tuple()
    num = sort_tuple_num(control)
    startTime = control[0]
    
    for i in num:
        time = control[i[0]+1];
        term_time = time - startTime;
        
        temp = (term_time, *i[1:]);
        re_control += (temp,);


def sort_tuple_num(control):
    num = tuple();
    
    for i in control[1:]:
        num += (i[0], )
        
    indexed_tuple = list(enumerate(num))  # [(index, value), ...]
    sort_num = sorted(indexed_tuple, key=lambda x: x[1])
    
    return sort_num

def encode_saver():
    global re_control
    return re_control;

i = 1
c = 1



def t(): 
    global c
    print(c)
    c += 1
    t1()

    
def t1():
    global c
    while c != 4:
        
        t()
    
    print('End')
        
t()
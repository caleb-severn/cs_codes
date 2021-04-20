# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:56:27 2021

@author: csevern
"""
#%% Method one, not entirely sure why this one didnt work
def isHappy(num):
        
    def square(numlist):
        v = sum([int(x)**2 for x in numlist])
        print(v)
        if len(str(v))> 1:
            square(list(str(v)))
            print("First",v)
            return True
        elif int(v) == 1:
            print("Second", v)
            return True
        elif int(v)>1 and len(str(v))==1:
            print("Third",v)
            return False
        else:
            print("Fourth", v)
            return False
    

    if num ==1:
        value = True
    elif num  <=3:
        value = False
    else:
        value = square(list(str(num)))
    return value;
        

print(isHappy(4))

#%%Method 2 This method is faster than 85% and more ram efficient than 92%

def isHappy(num):
    numlist = []
    while True:
        numlist.append(num)
        if num ==1:
            return True
            break
        elif num  <=3:
            return False
            break
        elif num in numlist[:-1]:
            return False
            break
        else:
            num = sum([int(x)**2 for x in list(str(num))])

         

            
print(isHappy(4))        
    
    
    
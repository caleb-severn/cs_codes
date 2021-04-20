# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 09:48:36 2021

@author: csevern
"""
#%% first attempt
import time
import random
dict_time = []
list_time = []
iteration = []
for t in range(0,100000000,10000000):
    randomnum = random.randint(t-10000000,t)
    start_time = time.time()
    Romans ={1000: 'M',900: 'CM',500: 'D',400: 'CD',100: 'C',90: 'XC',50: 'L',40: 'XL',10: 'X',9: 'IX',5: 'V',4: 'IV',1: 'I'}
    
    N_num=randomnum
    
    alt_num = N_num
    R_num=""
    
    while alt_num > 0:
    
        for i,v in Romans.items():
    
            if (alt_num/i) >= 1:
                l_num = v
                v_num = i
    
        R_num = R_num + str(l_num)
        alt_num = alt_num - v_num
    
    #print("Dictionaries", time.time()-start_time)    
    dict_time.append(time.time()-start_time)
    iteration.append(t)
    start_time = time.time()  
    RN = [1,4,5,9,10,40,50,90,100,400,500,900,1000]
    RL = ["I","IV","V","IX","X","XL","L","XC","C","CD","D","CM","M"]
    
    N_num=randomnum
    
    alt_num = N_num
    R_num=""
    
    while alt_num > 0:
    
        for i,v in enumerate(RN):
            if alt_num/v >= 1:
                l_num = RL[i]
                v_num = v
        R_num = R_num + str(l_num)
        alt_num = alt_num - v_num
    
    #print("Lists", time.time()-start_time)    
    list_time.append(time.time()-start_time)
    print(t)
    
import matplotlib.pyplot as plt
plt.plot(iteration, dict_time, label = "dictionary")
plt.plot(iteration, list_time, label = "lists")
plt.legend()
plt.show()

#%% second attempt

def romans(num):
    Romans ={1000: 'M',900: 'CM',500: 'D',400: 'CD',100: 'C',90: 'XC',50: 'L',40: 'XL',10: 'X',9: 'IX',5: 'V',4: 'IV',1: 'I'}
    Rom = ""
    print(num)
    while num > 0:
        for k, v in Romans.items():
  
            if (num/k) >= 1 :
                print(k, num)
                num = num-k
                Rom = Rom + v
                print(Rom)
                break
            

    return Rom
    
    
print(romans(1245))
        
    
    
    

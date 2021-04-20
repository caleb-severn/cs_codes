# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:52:14 2021

@author: csevern
"""
import random
test_list = [random.randint(0,100) for x in range(0,10001)]
#%% Successful attempt 1
import time
start_time = time.time()
def increasingTriplet(nums):
    Trip_TF = False
    for i,v in enumerate(nums):
        higher = [x for x in nums[i+1:] if x>v]
        for p,k in enumerate(higher[:-1]):
            if k<max(higher[p+1:]):
                Trip_TF=True
                break

    return Trip_TF

output = increasingTriplet(test_list)
print(output,time.time()-start_time)

#%% Optimised attempt 1 
import time
start_time = time.time()
def increasingTriplet(nums):
    Trip_TF = False
    for i,v in enumerate(nums[:-1]):
        list2 = [x for x in nums[i+1:] if x > v]
        if len(list2)>=2:
            minind = list2.index(min(list2))
            if minind <=len(list2)-2 and min(list2)<max(list2):
                Trip_TF = True
                break



    return Trip_TF

output = increasingTriplet(test_list)
print(output,time.time()-start_time)

#%% Optimised attempt 2 least ram option, mid speed option
import time
start_time = time.time()
def increasingTriplet(nums):
    Trip_TF = False
    minnum1= min(nums)
    maxnum1 =max(nums)
    for i,v in enumerate(nums[1:-1]):
        if v == minnum1 or v==maxnum1:
            continue
        i+=1
        maxnum = max(nums[i+1:])
        minnum = min(nums[:i])
        if minnum<v<maxnum:
            Trip_TF = True
            break
    
    return Trip_TF


output = increasingTriplet(test_list)
print(output,time.time()-start_time)

#%% Optimised attempt 3 from online solution that is much faster, but not less ram
import time
start_time = time.time()
def increasingTriplet(nums):
    first, second = float('inf'), float('inf')
    for num in nums:
        if num <= first:
            first = num
        elif num <= second:
            second = num
        else:
            return True
    return False

output = increasingTriplet([20,100,10,12,5,13])
#output = increasingTriplet([1,6,2,5,1])
#output = increasingTriplet([4,5,2147483647,1,2])
#output = increasingTriplet(test_list)
print(output,time.time()-start_time)
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 14:14:07 2021

@author: csevern
"""
#%% peak elements attempt 1, beats 91% on speed, 47% on memory

def peak(nums):
    maxind = nums.index(max(nums))
    if maxind == len(nums)-1 or  nums.index(max(nums)) == 0:
        peak = maxind
    elif len(nums)>= 3:
        peaks = [x+1 for x,v in enumerate(nums[1:-1]) if v>nums[x] and v>nums[x+2]]
        if len(peaks)>0:
            peak = peaks[0]
    else:
        peak = nums.index(max(nums))
    return peak;


output = peak([1,2,3])
print(output)

#%% try 2 faster than 74% and more ram efficient than 70.9%

def peak(nums):
    mn = max(nums)
    peak = nums.index(mn)
    for i in range(0,abs(min(nums)-max(nums))):
        maxind = nums.index((mn-i))
        if maxind < len(nums)-1:
            if nums[maxind-1]< ((mn-i)) and nums[maxind-1] < (mn-i):
                peak = maxind
                break
        else:
            peak = maxind
            break
    return peak
    


output = peak([1])
print(output)
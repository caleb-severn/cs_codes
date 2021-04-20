# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:10:31 2021

@author: csevern
"""
# All these sorting ones were super easy, so im including them in one code
#%% sort colors, when infact they're just numbers, don't ask me why, works in leetcode, however in spyder use sorted(nums) not sort()
def sortColors(nums):
    return nums.sort()
testlist = [0,2,1,2,1,1,0,2]
print(sortColors(testlist))

#%% Top-k elements
import random
testlist = [random.randint(1,100) for x in range(0,1000)]

import time
time_start = time.time()
def topKFrequent(nums, k):

    if k== len(nums):
        return nums
    else:
        numdict = {}
        for n in nums:
            if n in numdict.keys():
                numdict[n]+=1
            else:
                numdict[n]=1
        sortdict = {k: v for k, v in sorted(numdict.items(), key=lambda item: item[1], reverse = True)[:k]}
        print(sortdict)
    return list(sortdict.keys())
    
    

print(topKFrequent(testlist, k = 2), time.time()-time_start)


#%% K-largest element in an array, I mean its pretty easy

def findKthLargest(nums,k):
    nums = sorted(nums, reverse=True)
    return nums[k-1]

print(findKthLargest([1, 2, 2, 3, 3, 4, 5, 5, 6], 4))        

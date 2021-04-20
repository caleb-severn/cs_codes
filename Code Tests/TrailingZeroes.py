# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 10:01:54 2021

@author: csevern
"""
#%% works but not very fast or effecient
def trailingZeroes(n):
    factorial = n
    for i in range(1, n):
        factorial = factorial*i
    factorial = ''.join(reversed(str(factorial)))

    Zeroes = 0
    if len(factorial)>1 and int(factorial[0])==0:
        for num in factorial:
            if int(num)==0:
                Zeroes +=1
            else:
                break
    print(Zeroes)
    return Zeroes
        
trailingZeroes(0)

#%% Optimised with packages, better but still not fantastic
import math

def trailingZeroes(n):
    factorial = int(str(math.factorial(n))[::-1])
    Zeroes = 0
    if factorial[0] == 0:
        for i in range(0, len(factorial)):
            if factorial[i]==0:
                Zeroes +=1
            else:
                break
    return Zeroes
    
trailingZeroes(4)

#%% Actually use APE BRAIN with MATHEMATICS to solve, found math theory online
#However remember that on Leetcode its within a class so you need to include the class in the
#looping TrailingZeroes, pretty sure its Solution.trailingZeroes(self,n/5)

def trailingZeroes(n):
    #Just ignore anything under than 5
    if n<5:
        return 0
    return int(n/5) + int(trailingZeroes(n/5))

print(trailingZeroes(5))
    
    



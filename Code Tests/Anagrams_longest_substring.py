# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 15:10:41 2021

@author: csevern
"""
#%% anagrams
import collections
def anagram(str_list):
    ans = collections.defaultdict(list)

    for s in str_list:
        print(ans[tuple(sorted(s))],tuple(sorted(s)), s)
        ans[tuple(sorted(s))].append(s)
        
    return sorted(ans.values(), key=len)
        
                    
#list_ret = anagram(["","b"])    
list_ret = anagram(["eat","tea","tan","ate","nat","bat"])
print(list_ret)
#%% longest substring

def substring(string):
    """
    :type s: str
    :rtype: int
    """
    ans = 0
    sub = ''
    for char in string:
        print(char, sub)
        if char not in sub:
            sub += char
            ans = max(ans, len(sub))
        else:
            cut = sub.index(char)
            sub = sub[cut+1:] + char
    return ans
    


ans = substring("abcabccbb")
print(ans)           
#%% longest sequence Taken from stack overflow
#If you want to understand it, watch https://www.youtube.com/watch?v=Ns4LCeeOFS4&t=189s&ab_channel=GeeksforGeeks
#Look at my example below where I write a simplier version
            
def subseq(seq):
    if not seq:
        return seq

    M = [None] * len(seq)    # offset by 1 (j -> j-1)
    P = [None] * len(seq)

    # Since we have at least one element in our list, we can start by 
    # knowing that the there's at least an increasing subsequence of length one:
    # the first element.
    L = 1
    M[0] = 0

    # Looping over the sequence starting from the second element
    for i in range(1, len(seq)):
        # Binary search: we want the largest j <= L
        #  such that seq[M[j]] < seq[i] (default j = 0),
        #  hence we want the lower bound at the end of the search process.
        lower = 0
        upper = L

        # Since the binary search will not look at the upper bound value,
        # we'll have to check that manually
        print(seq[M[upper-1]], seq[i], M[upper-1])
        if seq[M[upper-1]] < seq[i]:
            j = upper

        else:
            # actual binary search loop
            print(upper, lower)
            while upper - lower > 1:
                mid = (upper + lower) // 2
                print(mid, seq[M[mid-1]])
                if seq[M[mid-1]] < seq[i]:
                    lower = mid
                else:
                    upper = mid
                    
            j = lower    # this will also set the default value to 0
        print(P,M)
        P[i] = M[j-1]
        #print(P,M)
        if j == L or seq[i] < seq[M[j]]:
            M[j] = i
            L = max(L, j+1)

    # Building the result: [seq[M[L-1]], seq[P[M[L-1]]], seq[P[P[M[L-1]]]], ...]
    result = []
    pos = M[L-1]
    for _ in range(L):
        result.append(seq[pos])
        pos = P[pos]

    return result[::-1]  
        
        
ans = subseq([0,3,4,7,5])
print(ans)          
    
#%% Longest increasing subsequence Caleb version
#watch https://www.youtube.com/watch?v=Ns4LCeeOFS4&t=189s&ab_channel=GeeksforGeeks
def subseq(seq):
    #An individual number is a longest subsequence of 1, so every value 
    #in the list has a longest subsequence of 1
    #LIS stands for longest increasing sequence
    LIS = [1]*len(seq)
    
    j= 0
    #Since the first position 0, already is a subsequence on its own
    #Start at position 2, i.e 1
    
    for i in range(1,len(seq)):
        #Is the value in position i, greater than the value in position j
        ival = seq[i]
        jval = seq[j]
        
        #if it is, add 1 to the LIS value for position i
        if ival > jval:
            LIS[i] +=1
            #Increase J's position by one
            j+=1
            #While j's position is less than current position, work your way
            #towards i, checking if the value in position j is less than the value
            #in position i, if the value is less, check if the subsequence value + 1
            #would be more or less than the LIS value in position i 
            while j < i:
                jval = seq[j]
                if jval < ival:
                    jlis = LIS[j]+1
                    if jlis > LIS[i]:
                        LIS[i] +=1 
                j+=1

        j=0
    print(LIS)
    return max(LIS)
                    
        
ans = subseq([10, 22,9,33,21,50,41,60])
print(ans)    
    
    
    
    

    
    
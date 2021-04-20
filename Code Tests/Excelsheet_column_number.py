# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 15:52:32 2021

@author: csevern
"""
#Take the column letters AA and translate it into column numbers, AA==27
#%% First try, turns out I'm a genius, its faster than 75% and more ram efficient than 92%
import string
def titleToNumber(title):
    number = 0
    for i,let in enumerate(''.join(reversed(title))):
        number += (26**(i))*(string.ascii_uppercase.index(let)+1)
    return number

print(titleToNumber("FXSHRXW"))
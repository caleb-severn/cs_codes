# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:58:55 2021

@author: csevern
"""
def setZeroes(matrix):
    """
    Do not return anything, modify matrix in-place instead.
    """
    index = list(set([i for row in matrix for i,v in enumerate(row) if v == 0]))
    for i, row in enumerate(matrix):
        if 0 in row:
            matrix[i] = [0]*len(row)
        else:
            for ind in index:
                matrix[i][ind]=0
    

setZeroes([[0,1,2,0],[3,4,5,2],[1,3,1,5]])
        
            
        
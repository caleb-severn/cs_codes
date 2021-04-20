# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 15:57:19 2021

@author: csevern
"""
#taken from the discussion pages really. I have no idea why they doing linked lists
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        cur = dummy
        
        carry = 0
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0
            
            # compute digit
            val = v1 + v2 + carry
            carry = val // 10
            val %= 10
            cur.next = ListNode(val)
            
            # update pointers
            cur = cur.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        
        return dummy.next
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 15:36:34 2021

@author: csevern
"""
import time
start_time = time.time()
def longestPalindrome(s):

    l_pal = ""
    if len(s)<=2:
        if ''.join(reversed(s))==s:
            l_pal=s
        else:
            l_pal=s[0]
    elif ''.join(reversed(s))==s:
        l_pal = s
    else:
        if len(s)>10 and len(s)/2  == int(len(s)/2):
            jump = 2
        elif len(s)>10 and len(s)/2  != int(len(s)/2):
            jump = 3
        else:
            jump = 1

        for i in range(0,len(s),jump):

            k=i
            p=i+1
            
            if ''.join(reversed(s[k:p]))==s[k:p]:
                
                while p<=len(s)-1 and k>=0:

                    if s[k-1:p+1]==''.join(reversed(s[k-1:p+1])):
                        if len(s[k-1:p+1])>len(l_pal):
                            l_pal=s[k-1:p+1]
                        k-=1
                        p+=1
                        next
                    elif s[k-1:p]==''.join(reversed(s[k-1:p])):
    
                        if len(s[k-1:p])>len(l_pal):
                            l_pal=s[k-1:p]
                        k-=1
                        next
                    elif s[k:p+1]==''.join(reversed(s[k:p+1])):

                        if len(s[k:p+1])>len(l_pal):
                            l_pal=s[k:p+1]
                        p+=1
                        next
                    else:
                        break
                    

  
 
                
    if len(l_pal)==0:
        l_pal=s[0]

           
    
    
    
    return l_pal
    
longest= longestPalindrome("anugnxshgonmqydttcvmtsoaprxnhpmpovdolbidqiyqubirkvhwppcdyeouvgedccipsvnobrccbndzjdbgxkzdbcjsjjovnhpnbkurxqfupiprpbiwqdnwaqvjbqoaqzkqgdxkfczdkznqxvupdmnyiidqpnbvgjraszbvvztpapxmomnghfaywkzlrupvjpcvascgvstqmvuveiiixjmdofdwyvhgkydrnfuojhzulhobyhtsxmcovwmamjwljioevhafdlpjpmqstguqhrhvsdvinphejfbdvrvabthpyyphyqharjvzriosrdnwmaxtgriivdqlmugtagvsoylqfwhjpmjxcysfujdvcqovxabjdbvyvembfpahvyoybdhweikcgnzrdqlzusgoobysfmlzifwjzlazuepimhbgkrfimmemhayxeqxynewcnynmgyjcwrpqnayvxoebgyjusppfpsfeonfwnbsdonucaipoafavmlrrlplnnbsaghbawooabsjndqnvruuwvllpvvhuepmqtprgktnwxmflmmbifbbsfthbeafseqrgwnwjxkkcqgbucwusjdipxuekanzwimuizqynaxrvicyzjhulqjshtsqswehnozehmbsdmacciflcgsrlyhjukpvosptmsjfteoimtewkrivdllqiotvtrubgkfcacvgqzxjmhmmqlikrtfrurltgtcreafcgisjpvasiwmhcofqkcteudgjoqqmtucnwcocsoiqtfuoazxdayricnmwcg")
#longest = longestPalindrome("caba")
print(longest)
print(time.time()-start_time)
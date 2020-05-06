#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:07:05 2020

@author: rjn
"""

import cv2
import numpy as np

def findline(img):
    '''

    Parameters
    ----------
    img : Array of uint8
        DESCRIPTION.

    Returns
    -------
    uppers : LIST
        list of upper boundary of text.
    lowers : LIST
        list of lower boundary of text.

    '''        
    # find and draw the upper and lower boundary of each lines
    hist = cv2.reduce(img,1, cv2.REDUCE_AVG).reshape(-1)
    th = 2
    uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
    lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]
    
    for y in range(len(uppers)):
        a = uppers[y]
        b = lowers[y]
        img = cv2.line(img,(0,a),(W,a),(255,0,0),2)
        img = cv2.line(img,(0,b),(W,b),(255,0,0),2)
    cv2.imshow("draw_line", img)     
    cv2.waitKey() 
    cv2.destroyAllWindows()
    cv2.imwrite('draw_line.png',img)
    return uppers, lowers

def separate_word(img,uppers,lowers):
    
    for y in range(len(uppers[:1])):
        a = uppers[y]
        b = lowers[y]
        
        roi = thresh[a-2:b+1,0:W+1]  
        roi = cv2.threshold(roi, 20, 255, cv2.THRESH_BINARY)[1]
        cnts, hie = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] * roi.shape[0] + cv2.boundingRect(ctr)[1], 
            reverse=False)
        for i,cnt in enumerate(cnts):
            if hie[0,i,3] == -1 or True:
                x,y,w,h = cv2.boundingRect(cnt)
                word = roi[y:y+h,x:x+w].copy()
                word = np.pad(word,4,mode='constant')                         
                rec = cv2.rectangle(roi.copy(),(x,y),(x+w,y+h), (255,0,40), 2)
                cv2.imwrite('5.png',rec)
                name = str(i) + '_sp.png' 
                cv2.imwrite(name,word)
                cv2.imshow("word", word)
                cv2.imshow("line_word", rec)     
                cv2.waitKey()                        
    cv2.destroyAllWindows()

img = cv2.imread('a.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray original", img)     
cv2.imwrite('orig.png',img)
H,W = img.shape[:2]

if (H < 600 or H > 1300) or(W < 600 or W > 1300):   
    if  (H < 600 or H > 1300): H = 600
    if  (W < 600 or W > 1300): W = 1300
    img = cv2.resize(img, (W,H), cv2.INTER_NEAREST) 
        
img = 255 - img
## (2) threshold
thresh =cv2.threshold(img,50,255,cv2.THRESH_BINARY)[1]
cv2.imshow("Threshold", thresh)     
cv2.waitKey() 
cv2.destroyAllWindows()
cv2.imwrite('thresh.png',thresh)
uppers, lowers = findline(thresh.copy())
separate_word(img,uppers,lowers)
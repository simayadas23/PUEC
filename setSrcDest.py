#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 18:48:00 2017

@author: tecnicmise
"""
def setSrcDest(mapno, AGVno): 
    if (AGVno == 1):
        if (mapno == 1):
            intSrc = 24
            intDst = 292               
        elif (mapno == 2):                
            intSrc = 16
            intDst = 303
        elif (mapno == 3):                
            intSrc = 1
            intDst = 313
        #end if
    elif (AGVno ==2):
        if (mapno == 1):
            intSrc = 6
            intDst = 312               
        elif (mapno == 2):                
            intSrc = 1
            intDst = 319
        elif (mapno == 3):                
            intSrc = 24
            intDst = 297
        #end if
    elif (AGVno ==3):
        if (mapno == 1):
            intSrc = 13
            intDst = 304               
        elif (mapno == 2):                
            intSrc = 10
            intDst = 315
        elif (mapno == 3):                
            intSrc = 12
            intDst = 311
        #end if
    elif (AGVno ==4):
        if (mapno == 1):
            intSrc = 13
            intDst = 303              
        elif (mapno == 2):                
            intSrc = 9
            intDst = 311
        elif (mapno == 3):                
            intSrc = 19
            intDst = 297
        #end if
        
    return intSrc, intDst

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:25:36 2017

@author: tecnicmise
"""
import os
from mapTopo import mapTopo
def createMaps(mapNo, rootDic):
    
    base_filename1 = 'map'
    suffix = '.txt'
    file_name1 = os.path.join(rootDic, base_filename1 + str(mapNo) + suffix)
    with open(file_name1, 'r') as gvnMap:
        OM = gvnMap.read()
    rowc = 16
    colc = 25
        
    mObj = mapTopo(OM,mapNo,rowc,colc)
        
    return mObj
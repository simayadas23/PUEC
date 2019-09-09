#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 15:33:53 2017

@author: tecnicmise
"""
import numpy as np
import os
class readObs():
    def __init__(self):
        self.d = {}
        dirName = "/home/pragna/Documents/PUEC/dataC/"
        arr_txt = [x for x in os.listdir(dirName) if x.endswith(".txt")]
        for f in arr_txt:
            f1=f.replace('C','m')[:-4]
            self.d[f1] = np.loadtxt(dirName+f)

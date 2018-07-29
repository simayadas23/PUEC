#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:10:25 2017

@author: tecnicmise
"""
#import numpy as np
from setSrcDest import setSrcDest
import os
from bModel import bModel
from dijsktraCost import dijsktraCost
import time
#import time
class AGV(dijsktraCost):
    "Creating the topo map from the given grid map"
    
    def __init__(self, rootDic, mapNo, noAGV, regNo, mObj):
        
        self.k = 0 
        self.all_path_cost=0        
        self.ownNo = noAGV        
        self.iSRC, self.iDST = setSrcDest(mapNo, noAGV)
        self.regNo = regNo
        self.bModObj = bModel(self.regNo)
        self.pathNo = 1
        self.mapNo = mapNo
        self.mObj = mObj
        self.dirName = rootDic
        self.baseN1 = 'Output'
        self.baseN2 = "avgAcRCYallPath"
        self.ownNo = noAGV
        self.suffix = '.txt'
        self.file1 = os.path.join(self.dirName, self.baseN1 + str(self.ownNo) + self.suffix)
        self.file2 = os.path.join(self.dirName, self.baseN2 + str(self.ownNo) + self.suffix)
        dijsktraCost.__init__(self,rootDic,regNo,mObj,self.iSRC,self.iDST)
    #end defn 
    def path(self):
        print('test')
        time.sleep(5)
    def pathPlanning(self,ontObjList):
        repNo = 100
        
        

        
        while self.pathNo <=repNo:
            ontObjList[self.ownNo-1].parseOnt(self.ownNo)
            acRYallP = self.findPath(self.k,ontObjList)
                    
            self.all_path_cost =self.all_path_cost+self.nPathCost
            print("Path found, path cost", self.nPath, self.nPathCost) 
            growingAvgPcost=self.all_path_cost/float(self.pathNo)
            outtxt1=str(self.mapNo)+' '+str(self.pathNo)+' '+' '+' '+str(growingAvgPcost)+str(self.nPath)+'\n'
            self.fid1 = open(self.file1,'a')
            self.fid1.write(outtxt1)
            self.fid1.close()
                
            self.k = self.k + self.lenPath                   
            self.pathNo = self.pathNo +1
            self.nPath.clear()		
            self.nPathCost = 0 
            ontObjList[self.ownNo-1].serializeOnt(self.ownNo)
        #end while      

        avgACRYaPath = acRYallP/self.pathNo
        fid2 = open(self.file2,'a')
        outtxt2 = str(repNo) + ' '+str(avgACRYaPath)+'\n' #' '+str(X_teqd)+
        fid2.write(outtxt2)
        fid2.close()
        self.all_path_cost = 0
        self.pathNo = 1
        self.k = 1
        

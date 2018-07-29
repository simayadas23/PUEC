#Main routin 
#import io
#import pythonds.basic.stack
#import math
#import os
from createMaps import createMaps
from AGV import AGV
from addNewTT import newTT
from newOntCreate import newOntCreate
from multiprocessing import Process,Queue
import sys
#import time

#def func(x):
#    
#    print(x*x)
#    time.sleep(5)
#    print(2*x)
if __name__ == "__main__":
    
        rootDic = sys.argv[1]
        totalAGVno = 4  
        regNo = 4 
        AGVObj=[]
        q = Queue()
        ontObjList =[]
        mapNo = 1 
        mObj = createMaps(mapNo, rootDic)  
            
        c = 1    
        while ( c <= totalAGVno):
            newOntCreate(c,rootDic)  
            AGVObj.append(AGV(rootDic,mapNo, c, regNo, mObj))
            ontObjList.append(newTT(c,rootDic))
            
            c = c+1
        #end while 
        q.put(ontObjList)    
        p1 = Process(target = AGVObj[0].pathPlanning,args=(ontObjList,))
        p2 = Process(target = AGVObj[1].pathPlanning,args=(ontObjList,))
        p3 = Process(target = AGVObj[2].pathPlanning,args=(ontObjList,))
        p4 = Process(target = AGVObj[3].pathPlanning,args=(ontObjList,))
        
        p1.start()
        p2.start()
        p3.start()
        p4.start()
#end main
    
    

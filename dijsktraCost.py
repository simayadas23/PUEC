#from AGV import AGV
from initialise import initialWeights
#from bilinear import bilinear_model
#from findWt import findWt
from find_adj import find_adj
#from form_end_state import form_end_state
from relax import relax
#from findLenPredecessor import findLenPredecessor
import numpy as np
#import pickle
from findWt import findWt
import os
class dijsktraCost:
    def __init__(self,rootDic,regNo,mObj,iSRC,iDST):
         
        self.phi = 0.2
        
        self.source = iSRC
        self.destination = iDST
        self.intialSRC = iSRC		
        self.intialDST = iDST
        self.regNo = regNo
        
        self.mObj = mObj 
        self.nPath = []
        self.lenPath = 0
        self.nPathCost = 0
        self.lastState = np.zeros((2*regNo+1))
        self.lastP = np.zeros((2*regNo+1,2*regNo+1))
        self.inPCurr = np.zeros((2*regNo+1,2*regNo+1))
        self.lastitrforOnt = 0
        self.estCount = 0
        self.growPerDiff = 0
        self.acRYallP  = 0       
        self.fObj = findWt(self.dirName,regNo,self.ownNo)
        self.dirName = rootDic
        self.base1 = "Own_TimeKf_U_PU"
        self.base2 = "AcRCYeachPath"
        self.base1 = "Own_TimeKf_U_PU"
        self.base3 = "Edges_u_d"
        self.suffix = '.txt'
        #self.ownNo = self.ownNo
        self.f1 = os.path.join(self.dirName, self.base1 + str(self.ownNo) + self.suffix)
        self.f2 = os.path.join(self.dirName, self.base2 + str(self.ownNo) + self.suffix)
        self.f3 = os.path.join(self.dirName, self.base3 + str(self.ownNo) + self.suffix)
        #self.fileO2 = os.path.join(self.dirName, self.base2 + self.no + self.suffix)
    def findPath(self,k,ontObjList, mapNo):
        print("Finding path in AGV ", self.ownNo )
        it = initialWeights(self.mObj,self.source)
        u = self.source
        itrforOnt = 0
        if (self.pathNo ==1):
            itrforOnt = 0
        elif (self.pathNo >1):
            itrforOnt = self.lastitrforOnt
        #print("Outside while:itrforfindNextX", itrforfindNextX)
        while len(it.Q)!= 0:                
            it.Q.remove(u) 
            self.findLenPredecessor(it, u)
            adj_u = find_adj(self.mObj,u)  
            seqNeigh = 0
            lenPrednodes = self.findLenPredecessor(it,u)
            #print("lenPrednodes", lenPrednodes)
            if (lenPrednodes):#cal_len_pred_nodes(it,self.source, u)
                timeKF = lenPrednodes+k+1  
            else:
                timeKF = k+1
                #print("timeKF",timeKF)
            #self.trackTimeKF.append(timeKF)
            predecessor_u = it.pi_v[u]
           # fid1 = open(self.f1,'a')
           # wrtxt1="AGvNo-"+str(self.ownNo)+" "+"U-"+str(u)+" "+"Pred-"+str(predecessor_u)+" "+"TimeKF-"+str(timeKF)+'\n' #' '+str(X_teqd)+
           # fid1.write(wrtxt1)
           # fid1.close()
            #print("ownNo, u,timeKF, pred of u",self.ownNo, u, timeKF,predecessor_u)
            if (predecessor_u == 0):
                if (self.pathNo >1):
                    self.inPCurr = self.lastP
                #end if 
            elif (predecessor_u != 0):
                if (timeKF > (self.regNo +1)): # and self.pathNo >=1):                        
                    self.inPCurr = self.fObj.P[predecessor_u][u]
                #end if
            #end if      
                     
            if (timeKF >= self.regNo):            
                self.bModObj.createModel(self.fObj,self.phi,lenPrednodes,
                            self.lastState,self.pathNo,self.regNo,timeKF,u,it)
            for h in adj_u:        #(vphi,len_pred_nodes,state_inp,path_no,n,time_KF,curr_node,it): 
                seqNeigh += 1            
                if h == 1:                
                    if (seqNeigh in self.mObj.neighbor_node_no[u]):
                        currNeighbor = self.mObj.neighbor_node_no[u][seqNeigh]
                    #end if 
                    if (currNeighbor !=self.source):
                        outtxt3 = str(mapNo) + ' ' + str(self.pathNo) + ' ' + str(self.ownNo) + ' ' + str(u) + ' ' + str(
                            currNeighbor) + '\n'
                        self.fid3 = open(self.f3, 'a')
                        self.fid3.write(outtxt3)
                        self.fid3.close()
                        itrforOnt = itrforOnt +1
                        #print("inside for and while:itrforfindNextX", itrforfindNextX)
                        self.estCount, self.growPerDiff, edgecost_to_neighbor = self.fObj.findNextX(ontObjList,itrforOnt, self.mObj,it,self.pathNo,
                            self.ownNo,self.regNo,self.inPCurr,seqNeigh,
                            currNeighbor,u,timeKF,self.source,self.bModObj)                            
                        relax(u,currNeighbor,it,edgecost_to_neighbor)                        
                    #end if 
                #end if
            #end for          
            #calculating min_d
            min_d  = float("inf")        
            for l in it.Q:
                    #print("l", l)
                if (it.d_v[l]< min_d):                 
                    min_d = it.d_v[l]                  
                #end if  
            #end for      
            for v, e in it.d_v.items():
                if e == min_d:                
                    if (v in it.Q):
                        nextU = v
                    #end if
                # end if
            # end for
            u = nextU
        
        #end of while loop 
        self.pathCost(it) #set path cost here
        self.formEndVars(it,self.bModObj,itrforOnt,ontObjList)
        return self.acRYallP# call end var here ??
    #end findPath
    def findLenPredecessor(self,it,curr_node):
        prev = 0 
        t = curr_node
        lenPrednodes = 0
        while (prev!=self.source):
            if (it.pi_v[t]!=0):
                prev = it.pi_v[t]
                lenPrednodes =lenPrednodes +1 #allPrev_nodes.append(prev)
                t = prev
            else:
                break
            #end if 
        #end while
        return lenPrednodes
    #end findLenPredecessor
    def pathCost(self,it):
            t = self.destination
            self.nPathCost = it.d_v[t]
            prev_node = 0 
            self.nPath.append(t)
            while (prev_node !=self.source):
        
                prev_node = it.pi_v[t]
                self.nPath.append(prev_node)
                t = prev_node    
            #end of while loop
            self.lenPath = len(self.nPath)
    def formEndVars(self,it,bModObj,itrforOnt,ontObjList):
        X = np.empty((self.regNo)) 
            #lastState = 
        cn=self.destination
        w =self.regNo-1
        while (w>=0):
            pred = it.pi_v[cn] 
                #print("cn, pred", cn, pred)
            if (pred == 0):
                X[w] = 0
                w = w-1
            else :            
                X[w] = self.fObj.edge_cost[pred][cn]
                cn = pred
                w =w -1
            #end if 
        #end while 
        self.lastState[0]= 1
        t=self.regNo
        for m in range(1,(self.regNo+1)):
            self.lastState[m] = bModObj.Ep[self.lenPath-t] 
            t = t -1
        #en for
        
        for o in range((self.regNo+1), ((2*self.regNo)+1)):
            self.lastState[o] = X[o-(self.regNo+1)]
                
        pred_current_target = it.pi_v[self.destination]
            #lastP = np.zeros((2*regNo+1,2*regNo+1))
            
        self.lastP=self.fObj.P[pred_current_target][self.destination]
            
            # interchange source destination
        if ((self.pathNo+1) == 45 or (self.pathNo+1) == 95):
            self.destination = self.intialDST
            self.source = self.intialSRC
        elif ((self.pathNo+1) >1 and (self.pathNo+1) != 45 and (self.pathNo+1) != 95):
            temp= self.destination
            self.source = temp
            if (((self.pathNo+1)%2)==0):
                if ((self.pathNo+1) == 44 or (self.pathNo+1) == 94):
                    if (self.mapNo ==1):
                        self.destination = self.intialSRC
                    elif (self.mapNo ==2):
                        self.destination = self.intialSRC
                    elif (self.mapNo ==3):
                        self.destination = self.intialSRC
                    #end if
                elif ((self.pathNo+1) != 44 and (self.pathNo+1) != 94):
                    if (self.mapNo ==1):
                        self.destination = 20
                    elif (self.mapNo ==2):
                        self.destination = 9
                    elif (self.mapNo ==3):
                        self.destination = 4
                    #end if
            elif (((self.pathNo+1)%2)!=0):
                if (self.mapNo ==1):
                    self.destination = 311
                elif (self.mapNo ==2):
                    self.destination = 314
                elif (self.mapNo ==3):
                    self.destination = 306
                #end if
        avgAcrcyP = self.growPerDiff/self.estCount
        self.acRYallP = self.acRYallP + avgAcrcyP
        fid2 = open(self.f2,'a')
        wrtxt2='Path:'+str(self.pathNo) + ' '+'Accry:'+str(avgAcrcyP)+'\n' #' '+str(X_teqd)+
        fid2.write(wrtxt2)
        fid2.close()
           
        self.lastitrforOnt = itrforOnt
        it.Q.clear()
        #for i in range(0, len(ontObjList)):
            #ontObjList[i].serializeOnt(self.ownNo)
    #end of form_end_state

            

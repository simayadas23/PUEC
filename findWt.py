#from bilinear import bilinear_model
from Kf import kalman
#from fetchObs import fetchOwnObs, fetchOtherObs
from statistics import mean
from collections import defaultdict#, OrderedDict
import os
import numpy as np
import pickle
#from obsMatrix import observationMean
from readObs import readObs
from addNewTT import newTT
#import time
class findWt(readObs):
    def __init__(self,rootDic,regN,ownNo):
        self.P = defaultdict(dict)
        self.XObs = defaultdict(dict)
        self.edge_cost = defaultdict(dict)
        self.sNext = np.empty([(2*regN+1),1])
        self.sCurr = np.empty([(2*regN+1),1])
        self.xObs = 0.00#np.empty([(2*regN+1),1])
        self.sMean = np.empty([(2*regN+1),1])
        self.PNext = np.empty([(2*regN+1), (2*regN+1)])
        self.PCurr = np.empty([(2*regN+1), (2*regN+1)])
        self.position = 2*regN
        self.trackTimeKF = []
        self.dirName = rootDic#'/home/tecnicmise/Dropbox/Dijkstra_widOntology/widOnt_v3'
        self.base1 = 'obsFrmOnt'
        self.base2 = 'obsFrmLegacy'
        self.no = str(ownNo)
        self.suffix = '.txt'
        self.file1 = os.path.join(self.dirName, self.base1 + self.no + self.suffix)
        self.file2 = os.path.join(self.dirName, self.base2 + self.no + self.suffix)
        self.estCount = 0
        self.growPerDiff = 0
        self.counterOnt = 0
        self.counterOwn = 0
        self.rootDic = rootDic
        readObs.__init__(self)
        newTT.__init__(self,ownNo,rootDic)
        self.kfObj = kalman(regN, ownNo)

        
        
                 #(self,regNo,inPCurr,seqNeigh,currNeighbor,currNode,tRegd,currentSource,bModObj)
    def findNextX(self,ontObjList,itrForOnt,mObj,it,pathNo, ownNO,regNo,inPCurr,seqNeigh,currNeighbor,
                  currNode,tRegd,currSource,bModObj):                  
        #########################################################################
        ### getting observation from other MRs                                ###
        ### if not available, getting from previous instance, or form legacy ####
        #########################################################################
        if (tRegd<=regNo):
            X_teqd = self.observationMean(seqNeigh,currNode)                      
        elif (tRegd > regNo):
            orig = currNode
            dest = currNeighbor            
                
   
            dictQres = ontObjList[ownNO-1].fetchOtherObs(ownNO,orig,dest,self.rootDic,ontObjList,tRegd)
            XReturn = []
            if (len(dictQres)!=0):
                self.fid1 = open(self.file1, 'a')
                for v, e in dictQres.items():
                    if (v == ownNO):
                        XReturn.append() = row[0]
                            k = row[1]
                            XReturn = float(XReturn)
                            k = int(k)
                            self.XObs[k] = XReturn 
                        #end for
                    #end if
                #end for
                
                maxKey = max(self.XObs, key=int)
                self.xObs = self.XObs[maxKey]
                self.counterOnt += self.counterOnt
                outtxt1 = str(pathNo) + ' ' + str(ownNO) + ' ' + str(self.counterOnt) + ' ' + str(self.xObs) + '\n'  # ' '+str(X_teqd)+
                self.fid1.write(outtxt1)
                self.fid1.close()
            else:
                if (currNode != currSource):
                    orig=it.pi_v[currNode]
                    dest = currNode
                    self.xObs = self.edge_cost[orig][dest]
                    self.counterOwn += self.counterOwn
                    outtxt2 = str(pathNo) + ' ' + str(ownNO) + ' ' + str(self.counterOnt) + ' ' + str(self.xObs) + '\n'
                    self.fid2 = open(self.file2, 'a')
                    self.fid2.write(outtxt2)
                    self.fid2.close()
                elif (currNode == currSource):
                    self.getLegacy(mObj, currNode, seqNeigh, tRegd)
                    outtxt2 = str(pathNo) + ' ' + str(ownNO) + ' ' + str(self.counterOnt) + ' ' + str(self.xObs) + '\n'
                    self.fid2 = open(self.file2, 'a')
                    self.fid2.write(outtxt2)
                    self.fid2.close()
                #end if
            self.XObs.clear() 
            
            ####################################################
            ### starting state and calculating covariance P  ###                            
            ####################################################          
            
            if (pathNo == 1 and tRegd == (regNo+1)): #and currNode == currSource):
                self.sMean[0] = 1
                d = regNo
                for m in range(1,(regNo+1)):
                    self.sMean[m] = bModObj.Ep[(tRegd-d)]
                    d = d -1
                #end for 
                orig=it.pi_v[currNode]
                dest =currNode
                itr = (tRegd-1)
                #print("Creating sPrev")
                for a in range(0,regNo):
                    if (orig!=0):
                        #print("orig, dest", orig, dest)                        
                        obsMean = self.getMeanLegacy(itr)#self.getLegacy(mObj, orig, dest, itr)
                        #print("obs after return", obs)
                        self.sMean[(2*regNo)-a] = obsMean
                        itr = itr -1
                        dest = orig
                        orig = it.pi_v[orig]
                    #end if                    
                #end for
                try:                    
                    minus = bModObj.state_vector_curr-self.sMean
                    transPoseMinus = np.transpose(minus)
                    prodCovP = np.dot(minus,transPoseMinus)
                    self.PCurr = np.mean(prodCovP)#np.identity((2*regNo+1))#np.cov(bModObj.state_vector_curr,self.sMean) #np.mean(prod.flatten())
                    self.sCurr = self.sMean#np.cov(bModObj.state_vector_curr - self.sPrev)#
                    #print ("self.PCurr",self.PCurr)
                except: 
                    print("inside except")
                    print("self.sPrev", self.sMean)
                    print("bModObj.state_vector_curr", bModObj.state_vector_curr)
                    #print("prod", prod)
            else:
                self.PCurr = inPCurr
                self.sCurr = bModObj.state_vector_curr 
            ###############################################
            ### Kalman Filter called to obtain estimate ###
            ###############################################
            self.sNext, self.PNext = self.kfObj.KF(bModObj.Ep[tRegd-1],tRegd,self.sCurr,bModObj.F,bModObj.V,bModObj.G,bModObj.H,bModObj.Q,bModObj.R,self.PCurr,self.xObs)
            
            self.P[currNode][currNeighbor] = self.PNext
            X_teqd = self.sNext[self.position]
            X_teqd = X_teqd[0]
                        #,mObj, i, neighbor_no, itr):
            self.getLegacy(mObj, currNode, seqNeigh, tRegd)
            self.accRCY(X_teqd, self.xObs)
            self.estCount = self.estCount +1
        if X_teqd <0:
            with open('objsnegcost.pickle', 'wb') as f:
                pickle.dump([pathNo,currNode,tRegd,currNeighbor,bModObj.state_vector_curr,self.sObs,self.PCurr,self.PNext,currSource], f)
        #print("Inside findNextX,itr", itrForOnt)
        ontObjList[ownNO-1].addNewTT(regNo, currNode, currNeighbor, tRegd, itrForOnt, X_teqd, ownNO)
        
        self.edge_cost[currNode][currNeighbor] = X_teqd
        
        return self.estCount, self.growPerDiff, X_teqd
    def observationMean(self, neighbor_no,i):
        if (neighbor_no == 1 or neighbor_no == 3 or neighbor_no == 5 or neighbor_no == 7):
            if (i == 230 or i == 231 or i == 232 or i == 233 or i == 234 or i == 259 or i == 260 or i == 261 or i == 262 or i == 263 or i == 288 or i == 289 or i == 290 or i == 291 or i ==292 or i == 317 or i == 318 or i == 319 or i == 320 or i == 321 or i == 344 or i == 345 or i == 346 or i == 347 or i == 348 or i == 367 or i == 368 or i == 369 or i == 370 or i == 371):  
                                                       
                meanData = np.mean(self.d['m17s'])
            if (i == 593 or i == 594 or i == 595 or i == 596 or i == 597 or i == 598 or i == 599 or i == 600 or i == 622 or i == 623 or i == 624 or i == 625 or i == 626 or i == 627 or i == 628 or i == 629 or i == 630 or i == 652 or i == 653 or i == 654 or i == 655 or i == 656 or i == 657 or i == 658 or i== 659 or i == 660 or i == 682 or i == 683 or i == 684 or i == 685 or i == 686 or i == 687 or i == 688 or i == 689 or i == 690 or i == 708 or i == 709 or i == 710 or i == 711 or i == 712 or i == 713 or i == 714 or i == 715 or i == 716 or i == 731 or i == 732 or i == 733 or i == 734 or i == 735 or i == 736 or i == 737 or i == 738 or i == 739 or i == 755 or i == 756 or i == 757 or i == 758 or i == 759 or i == 760 or i == 761 or i == 762 or i == 763 or i == 377 or i == 378 or i == 379 or i == 380 or i == 381 or i == 400 or i == 401 or i == 402 or i == 403 or i == 404 or i == 423 or i == 424 or i == 425 or i == 426 or i == 427):
            
                meanData = np.mean(self.d['m17sp'])
            else:
                meanData = np.mean(self.d['m17p'])
        elif (neighbor_no == 2 or neighbor_no == 4 or neighbor_no == 6 or neighbor_no == 8):
                if (i == 230 or i == 231 or i == 232 or i == 233 or i == 234 or i == 259 or i == 260 or i == 261 or i == 262 or i == 263 or i == 288 or i == 289 or i == 290 or i == 291 or i ==292 or i == 317 or i == 318 or i == 319 or i == 320 or i == 321 or i == 344 or i == 345 or i == 346 or i == 347 or i == 348 or i == 367 or i == 368 or i == 369 or i == 370 or i == 371):  
                                                     
                    meanData = np.mean(self.d['m24s'])
                if (i == 593 or i == 594 or i == 595 or i == 596 or i == 597 or i == 598 or i == 599 or i == 600 or i == 622 or i == 623 or i == 624 or i == 625 or i == 626 or i == 627 or i == 628 or i == 629 or i == 630 or i == 652 or i == 653 or i == 654 or i == 655 or i == 656 or i == 657 or i == 658 or i== 659 or i == 660 or i == 682 or i == 683 or i == 684 or i == 685 or i == 686 or i == 687 or i == 688 or i == 689 or i == 690 or i == 708 or i == 709 or i == 710 or i == 711 or i == 712 or i == 713 or i == 714 or i == 715 or i == 716 or i == 731 or i == 732 or i == 733 or i == 734 or i == 735 or i == 736 or i == 737 or i == 738 or i == 739 or i == 755 or i == 756 or i == 757 or i == 758 or i == 759 or i == 760 or i == 761 or i == 762 or i == 763 or i == 377 or i == 378 or i == 379 or i == 380 or i == 381 or i == 400 or i == 401 or i == 402 or i == 403 or i == 404 or i == 423 or i == 424 or i == 425 or i == 426 or i == 427):
               
                    meanData = np.mean(self.d['m24f'])
                else:
                    meanData = np.mean(self.d['m24p'])
                #end if 
        #end if 

        return meanData
    def getMeanLegacy(self, itr):
        obs = [] 
#d['m17p'][0]                 #x[i,j,:] = d1                            
        obs.append(self.d['m17s'][itr])           
        obs.append(self.d['m17p'][itr])            
        obs.append(self.d['m17sp'][itr])            
        obs.append(self.d['m17p'][itr])                               
        obs.append(self.d['m24s'][itr])                
        obs.append(self.d['m24p'][itr])                
        obs.append(self.d['m24f'][itr])                
        obs.append(self.d['m24p'][itr])                
        obsMean = mean(obs)
        return obsMean
    
    def getLegacy(self,mObj, i, neighbor_no, itr):
#        rowNo = i
#        print("rowNo:", rowNo)
#        xx=mObj.neighbor_node_no[rowNo]
#        print("xx:", xx)
#        neighbor_no = (list(xx.keys())[list(xx.values()).index(dest)])
        #neighbor_no = np.where(mObj.neighbor[rowNo]==dest)[0]
        if (neighbor_no == 1 or neighbor_no == 3 or neighbor_no == 5 or neighbor_no == 7):
            if (i == 230 or i == 231 or i == 232 or i == 233 or i == 234 or i == 259 or i == 260 or i == 261 or i == 262 or i == 263 or i == 288 or i == 289 or i == 290 or i == 291 or i ==292 or i == 317 or i == 318 or i == 319 or i == 320 or i == 321 or i == 344 or i == 345 or i == 346 or i == 347 or i == 348 or i == 367 or i == 368 or i == 369 or i == 370 or i == 371):  
                                                 
                self.xObs=self.d['m17s'][itr]
            else:
                self.xObs=self.d['m17p'][itr]
            if (i == 593 or i == 594 or i == 595 or i == 596 or i == 597 or i == 598 or i == 599 or i == 600 or i == 622 or i == 623 or i == 624 or i == 625 or i == 626 or i == 627 or i == 628 or i == 629 or i == 630 or i == 652 or i == 653 or i == 654 or i == 655 or i == 656 or i == 657 or i == 658 or i== 659 or i == 660 or i == 682 or i == 683 or i == 684 or i == 685 or i == 686 or i == 687 or i == 688 or i == 689 or i == 690 or i == 708 or i == 709 or i == 710 or i == 711 or i == 712 or i == 713 or i == 714 or i == 715 or i == 716 or i == 731 or i == 732 or i == 733 or i == 734 or i == 735 or i == 736 or i == 737 or i == 738 or i == 739 or i == 755 or i == 756 or i == 757 or i == 758 or i == 759 or i == 760 or i == 761 or i == 762 or i == 763 or i == 377 or i == 378 or i == 379 or i == 380 or i == 381 or i == 400 or i == 401 or i == 402 or i == 403 or i == 404 or i == 423 or i == 424 or i == 425 or i == 426 or i == 427):
           
                self.xObs=self.d['m17sp'][itr]
            else:
                self.xObs=self.d['m17p'][itr]
        elif (neighbor_no == 2 or neighbor_no == 4 or neighbor_no == 6 or neighbor_no == 8):
            if (i == 230 or i == 231 or i == 232 or i == 233 or i == 234 or i == 259 or i == 260 or i == 261 or i == 262 or i == 263 or i == 288 or i == 289 or i == 290 or i == 291 or i ==292 or i == 317 or i == 318 or i == 319 or i == 320 or i == 321 or i == 344 or i == 345 or i == 346 or i == 347 or i == 348 or i == 367 or i == 368 or i == 369 or i == 370 or i == 371):  
                                                       
                self.xObs=self.d['m24s'][itr]
            else:
                self.xObs=self.d['m24p'][itr]
            if (i == 593 or i == 594 or i == 595 or i == 596 or i == 597 or i == 598 or i == 599 or i == 600 or i == 622 or i == 623 or i == 624 or i == 625 or i == 626 or i == 627 or i == 628 or i == 629 or i == 630 or i == 652 or i == 653 or i == 654 or i == 655 or i == 656 or i == 657 or i == 658 or i== 659 or i == 660 or i == 682 or i == 683 or i == 684 or i == 685 or i == 686 or i == 687 or i == 688 or i == 689 or i == 690 or i == 708 or i == 709 or i == 710 or i == 711 or i == 712 or i == 713 or i == 714 or i == 715 or i == 716 or i == 731 or i == 732 or i == 733 or i == 734 or i == 735 or i == 736 or i == 737 or i == 738 or i == 739 or i == 755 or i == 756 or i == 757 or i == 758 or i == 759 or i == 760 or i == 761 or i == 762 or i == 763 or i == 377 or i == 378 or i == 379 or i == 380 or i == 381 or i == 400 or i == 401 or i == 402 or i == 403 or i == 404 or i == 423 or i == 424 or i == 425 or i == 426 or i == 427):
                
                self.xObs=self.d['m24f'][itr]
            else:
                self.xObs=self.d['m24p'][itr]
        #end if 
        
        #return obs
    def accRCY(self, estX, legX):
        perDiff = ((estX-legX)/legX)*100
        self.growPerDiff = self.growPerDiff + perDiff
    #end accRCY
    
    







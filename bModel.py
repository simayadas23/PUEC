import numpy as np
#import os
#import math
#from collections import defaultdict
class bModel:
    "Create matrices"
    def __init__(self,regN):        
        self.state_vector_curr = np.empty([(2*regN+1),1])
        #self.P = []
        self.Ep = np.random.normal(0.1, 0.1, 4212)
        #self.X_all = []
        self.F = np.zeros([(2*regN+1),(2*regN+1)])
        self.V = np.zeros([(2*regN+1),1])
        self.G = np.identity((2*regN+1))#np.zeros((2*regN+1))
        self.H = np.zeros([1,(2*regN+1)])
        self.SHAI = np.empty((regN))
        self.PHI = np.empty((regN))        
        self.B = np.random.normal(0.1, 0.1, regN)
        self.C = np.random.normal(0.1, 0.1, (regN,regN)) 
        self.w = np.random.normal(0,0.1,4212)
        self.v = np.random.normal(0,0.1,4212) 
        #self.probW = np.repeat(1/1000, (2*regN+1))
        #self.probV = np.repeat(1/1000, (2*regN+1))
        self.Q = 0.00
        self.R = 0.00
        self.V[regN] = 1
        self.V[2*regN] = 1#+1)-1] = 1        
        self.H[0][2*regN] = 1
        #self.formAutoCov()
        
    def createModel(self,fObj,vphi,len_pred_nodes,state_inp,path_no,n,time_KF,curr_node,it): 
        X = np.zeros((n)) 
        sumC = 0 
        pred = 0
        
        if (path_no>1):
            
            cn = curr_node
            w = n-1
            r =0
            while (w>=0):
                pred = it.pi_v[cn]            
                if (pred == 0):
                    
                    X[w]=state_inp[(2*n)-r]
                    r=r+1         
                    w=w-1
                else:#:            
                    X[w] =fObj.edge_cost[pred][cn]
                    #if (curr_node == 256):
                        #print("X[w]", X[w])
                    cn = pred 
                    w=w-1
                #end if
            #end while
            
            constant_miu = np.mean(X)
            self.state_vector_curr[0]= 1       
        
            t=n
            for m in range(1,(n+1)):
                self.state_vector_curr[m] = self.Ep[(time_KF-t)] 
                t=t-1
            #end for
            for o in range((n+1), ((2*n)+1)):
                self.state_vector_curr[o] = X[o-(n+1)]
            
        elif (path_no ==1):      
            
            cn = curr_node
            w = n-1
            while (w>=0):
                pred = it.pi_v[cn]            
                if (pred == 0):
                    X[w] = 0
                    w = w-1
                else :            
                    X[w] = fObj.edge_cost[pred][cn]
                    cn = pred
                    w =w -1
                #end if 
            #end while 
        
            constant_miu = np.mean(X)
            self.state_vector_curr[0]= 1
            t=n           
            for m in range(1,(n+1)):
                self.state_vector_curr[m] = self.Ep[(time_KF-t)] 
                t=t-1
            #end for
        
            for o in range((n+1), ((2*n)+1)):
                self.state_vector_curr[o] = X[o-(n+1)]
            #end for
        
        shai = np.ones(n)*10
        phi = np.ones(n)*10
        for z in range(0,len(shai)):
            for p in range(0,len(shai)):
                sumC = sumC + self.C[z][p]*X[(n-1)-p]
            #end for
            shai[z]=self.B[z]+sumC
            sumC =0
            phi[z] = vphi
        #end for 
        
        a = np.ones((n,), dtype=np.int)*n
        b = range(0,(n))
        c = a-b
        d = c*(-1)
        s = [0]
        index = np.concatenate((s,c, d), axis=0)
        #print(index)
        r = 1
        for w in range(1,(2*n+1)):
            if (index[w]> 0):
                row = n - abs(index[w])
                #print('row in if',row)
            else: 
                row = n - abs(index[w])
                if row>0:
                    row=row+n
    
                    #print('row in else',row)
            #end if  
            if row >0:
                self.F[row][w] =1
            #end if
            if w <=n:
                #print('value of w, when it is less than or equal to reg_n:',w)
                self.F[(2*n+1)-1][w] = shai[n-w]
            elif w<=(2*n+1) and w > n:
                #print('value of w, when it is greater than reg_n and less than or equal to 2*reg_n+1:',w)
                self.F[(2*n+1)-1][w] = (-1)*phi[w-(2*r)]    
                r = r+1
            #end if   
        # end for
        self.F[0][0]=1
        self.F[(2*n+1)-1][0] = constant_miu        
        
        self.SHAI = shai
        self.PHI = phi
        
        def formAutoCov(self,time_KF): 
        #p1,q1 = (np.shape(self.w))
        #p2,q2 = (np.shape(self.v))
        #var = 0.0001
        #for i in range(0, q1):
#            for j in range(0,q1):
#                if (i==j):
            self.Q = np.cov(self.w[time_KF],self.w[time_KF])
            self.R = np.cov(self.v[time_KF],self.v[time_KF])
#        for i in range(0, q2):
#            for j in range(0,q2):
#                if (i==j):
                    
        

            
        
        
        #return state_vector_x, f, g, h, shai, phi

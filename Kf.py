import numpy as np
#import os
#from numpy.linalg import inv
    #(Ep,tRegd,state,regNo,F,V,G,H,R,Y,PCurr,self.sObs)
class kalman():
    def __init__(self,reg_n,ownNo):
        self.reg_n = reg_n
        self.Kalman_gain = np.empty((2*self.reg_n+1))    
        self.state_apriori = np.empty((2*self.reg_n+1))
        self.next_estimate = np.empty((2*self.reg_n+1))
#        self.dirName = '/home/tecnicmise/Dropbox/Dijkstra_widOntology/widOnt_v3'
#        self.base1 = 'InpKF'
#        self.base2 = 'PCycle'
#        self.base3 = 'CCycle'
        #self.no = str(ownNo)
#        self.suffix = '.txt'
#        self.file1 = os.path.join(self.dirName, self.base1 + self.no + self.suffix)
#        self.file2 = os.path.join(self.dirName, self.base2 + self.no + self.suffix)
#        self.file3 = os.path.join(self.dirName, self.base3 + self.no + self.suffix)
    def KF(self,Ep_reqd,t_reqd,state,F,V,G,H,Q,R,P_prev,y_t):
        #print input variables in file
#        fid1 = open(self.file1,'a')
#        wrtxt1='TimeKF-'+str(t_reqd) + ' '+ 'State_Curr-'+str(state) + ' '+ 'Ep_tRegd-'+str(Ep_reqd) + ' '+'F-'+str(F)+' '+'V-'+str(V)+' '+'G-'+str(G)+' '+'H-'+str(H)+' '+'Q-'+str(Q)+' '+'R-'+str(R)+' '+'PCurr-'+str(P_prev)+' '+'Obs-'+str(y_t)+'\n' #' '+str(X_teqd)+
#        fid1.write(wrtxt1)
#        fid1.close()
        #prediction cycle
        f1 = np.dot(F,state)
        f2 = np.dot(V, Ep_reqd) 
        state_apriori = f1 + f2     #np.dot(F,state) + np.dot(V, Ep[t_reqd]) 
    
        first = np.dot(F, (np.dot(P_prev,np.transpose(F))))
   
        second = np.dot(G,(np.dot(Q,np.transpose(G))))
    
        P_apriori = first + second
#        fid2 = open(self.file2,'a')
#        wrtxt2='TimeKF-'+str(t_reqd) + ' '+ 'f1-'+str(f1) + ' '+ 'f2-'+str(f2) + ' '+'sApriori-'+str(state_apriori)+' '+'first-'+str(first)+' '+'Second-'+str(second)+' '+'PApriori-'+str(P_apriori)+'\n' #' '+str(X_teqd)+
#        fid2.write(wrtxt2)
#        fid2.close()
        #Correction cycle
    
        interS= np.dot(np.dot(H,P_apriori),np.transpose(H))
    
        prodS = (interS+R)
   
#    #if (np.isscalar(prodS)):
#        print("yes scalar")
#        Kalman_gain = np.dot(P_apriori,np.dot(np.transpose(H),(1/prodS)))
#    else:
   # Kalman_gain = np.dot(P_apriori,np.multiply(np.transpose(H),inv(prodS)))
        K1 = np.dot(P_apriori,np.transpose(H))
        Kalman_gain = np.dot(K1,1/(prodS))
    #end if
    #print("Kalman_gain: ", Kalman_gain)
    #print("y_t: ", y_t)
        j = np.dot(H,state_apriori)
    #print("j", j)
    #print("y_t", y_t)
        next_estimate = state_apriori + np.dot(Kalman_gain,(y_t-j))
        #print("next_estimate", next_estimate)
#        fid3 = open(self.file3,'a')
#        wrtxt3='TimeKF-'+str(t_reqd) + ' '+ 'interS-'+str(interS) + ' '+ 'prodS-'+str(prodS) + ' '+'K1-'+str(K1)+' '+'Kalman_gain-'+str(Kalman_gain)+' '+'j-'+str(j)+' '+'next_estimate-'+str(next_estimate)+'\n' #' '+str(X_teqd)+
#        fid3.write(wrtxt3)
#        fid3.close()
          
    
        P_next = P_apriori- Kalman_gain*H*P_apriori
    

        return next_estimate, P_next


    #return tao_hat_next, P_next
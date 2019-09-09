#import numpy as np
#import math
class initialWeights:
    "Initialise d and pi"
    
    
    
    def __init__(self, mapObj, u):
        self.d_v = {}
        self.pi_v = {}
        self.Q = dict()
        self.Q = [row[0] for row in mapObj.node]
        
        for y in self.Q:
    
            if self.Q[y-1]!=u:
    
                v = self.Q[y-1]
                #print ("v in initialise:", v)
                self.d_v[v] = float("inf")
                #print "d_v[v]", d_v[v]
                self.pi_v[v] = 0
            elif self.Q[y-1] == u:
                self.d_v[u]= 0
                self.pi_v[u] = 0
            #end if
        #end for 
        

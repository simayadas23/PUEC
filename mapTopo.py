from collections import defaultdict
import math
#import os
#import numpy as np
class mapTopo:
    "Creating the topo map from the given grid map"
    node = []
    neighbor = []
    neighbor_node_no = defaultdict(dict)
    edge = []
    port = []
    no_of_nodes = 0    
    def __init__(self, gM, mapno, rowcount,colcount):

        def hex2int(ch):
            v = 0;
            hex1 = '0123456789abcdef';
            if len(ch) == 1:
                v = hex1.find(ch)
                #end if
            return v        
        # end of hex2int
        
        newport = []
        newnode = []
        newneighbor = []         
        p = 0
        n = 0
        i = 0
        rowpos = 0
        colpos = 0    
        noEdges = 0
        g = gM.replace('\n','')
        #print "Length of g", len(g)

        while (i < len(g)): 
            w = g[i]
            rowpos = math.floor((i)/colcount)
            colpos = i% colcount
            if w != '.':
                v = hex2int(w)
                #print v

                if v > 0:
                # print "rowpos,colpos",rowpos,colpos
                    newport = [v, rowpos, colpos]
                    self.port.append(newport)
                    p +=1
                    #end if  
            
            #end if  
            if w == '.':
                n +=1
                file1 = open('nNODE.txt', 'a')
                file2 = open('nNEIGHBOR.txt', 'a')
                newnode = [n,rowpos,colpos]
                nodeStr = str(newnode)+'\n'			
                file1.write(nodeStr) 
                file1.close()
                self.node.append(newnode)  
                leftcol = max((colpos-1),0) 
    
                rightcol = min((colpos+1),(colcount-1))
                toprow = max((rowpos-1),0)
                bottomrow = min((rowpos +1),(rowcount-1))
                diagonal_left_bottomrow = min((rowpos +1),(rowcount-1))
                diagonal_left_bottomcol = max((colpos -1),0)
                diagonal_right_bottomrow = min((rowpos +1),(rowcount-1))
                diagonal_right_bottomcol = min((colpos +1),(colcount-1))
                diagonal_right_toprow = max((rowpos -1),0)
                diagonal_right_topcol = min((colpos +1),(colcount-1))
                diagonal_left_toprow = max((rowpos -1),0)
                diagonal_left_topcol = max((colpos-1),0)
    
                index_Left = (((rowpos)*colcount)+leftcol)
    
                index_Right = (((rowpos)*colcount)+rightcol)
                index_Top = (((toprow)*colcount)+colpos)
                index_Bottom = (((bottomrow)*colcount)+colpos)
    
                index_topLeft_diagonal = (((diagonal_left_toprow )*colcount) + diagonal_left_topcol)
    
                index_topRight_diagonal = (((diagonal_right_toprow )*colcount) + diagonal_right_topcol)
                index_bottomLeft_diagonal = (((diagonal_left_bottomrow )*colcount) + diagonal_left_bottomcol)
                index_bottomRight_diagonal = (((diagonal_right_bottomrow )*colcount) + diagonal_right_bottomcol) 
    
                if ( index_Left != i):
                    neighbour_left = g[int(index_Left)]
                    if (neighbour_left == '.'):
                        neighbour_left = 1
                        edge_left = 1
                        noEdges = noEdges + 1
                    else: 
                        neighbour_left = 0
                        edge_left = 0 
                    #end if    
                else:
                    neighbour_left = -1
                    edge_left = -1
                #end if 
                if (index_Right != i): 
                    neighbour_right = g[int(index_Right)] 
                    if (neighbour_right == '.'):
                        neighbour_right = 1
                        edge_right = 1
                        noEdges = noEdges + 1
                    else:
                        neighbour_right = 0
                        edge_right = 0
                    #end if    
                else:
                    neighbour_right = -1
                    edge_right = -1  
                #end if
                if (index_Top != i):
                    neighbour_top = g[int(index_Top)]
                    if (neighbour_top == '.'):
                        neighbour_top = 1
                        edge_top = 1
                        noEdges = noEdges + 1
                    else:
                        neighbour_top = 0
                        edge_top = 0
                    #end if     
                else:
                    neighbour_top = -1
                    edge_top = -1   
                #end if
                if (index_Bottom != i): 
                    neighbour_bottom = g[int(index_Bottom)]  
                    if (neighbour_bottom == '.'):
                        neighbour_bottom = 1
                        edge_bottom = 1
                        noEdges = noEdges + 1
                    else:
                        neighbour_bottom = 0
                        edge_bottom = 0
                else:
                    neighbour_bottom = -1
                    edge_bottom = -1
                #end if
                if ( index_Left != index_topLeft_diagonal and index_Top !=index_topLeft_diagonal):
                    neighbor_topLeft = g[int(index_topLeft_diagonal)]
    
                    if (neighbor_topLeft == '.'):
                        neighbor_topLeft = 1
                        edge_topLeft = 1
                        noEdges = noEdges + 1
                    else:
                        neighbor_topLeft = 0
                        edge_topLeft = 0
                    #end if    
                else:
                    neighbor_topLeft = -1
                    edge_topLeft = -1
                #end if
                if (  index_Right != index_topRight_diagonal and index_Top != index_topRight_diagonal):
                    neighbor_topRight = g[int(index_topRight_diagonal)]
                    if (neighbor_topRight == '.'):
                        neighbor_topRight = 1
                        edge_topRight = 1
                        noEdges = noEdges + 1
                    else:
                        neighbor_topRight = 0
                        edge_topRight = 0
                    #end if    
                else: 
                    neighbor_topRight = -1
                    edge_topRight = -1
                #end if
                if ( index_Left != index_bottomLeft_diagonal and index_Bottom !=index_bottomLeft_diagonal):
                    neighbor_bottomLeft = g[int(index_bottomLeft_diagonal)]
                    if (neighbor_bottomLeft == '.'):
                        neighbor_bottomLeft = 1
                        edge_bottomLeft = 1
                        noEdges = noEdges + 1
                    else:
                        neighbor_bottomLeft = 0
                        edge_bottomLeft = 0
                    #end if    
                else:
                    neighbor_bottomLeft = -1
                    edge_bottomLeft = -1
                #end if
                if ( index_Right != index_bottomRight_diagonal and index_Bottom != index_bottomRight_diagonal):
                    neighbor_bottomRight = g[int(index_bottomRight_diagonal)]
                    if (neighbor_bottomRight == '.'):
                        neighbor_bottomRight = 1
                        edge_bottomRight = 1
                        noEdges = noEdges + 1
                    else:
                        neighbor_bottomRight = 0
                        edge_bottomRight = 0
                    #end if    
                else:
                    neighbor_bottomRight = -1
                    edge_bottomRight = -1
                #end if
                newneighbor = [neighbour_left,neighbor_topLeft,neighbour_top,neighbor_topRight,
                               neighbour_right, neighbor_bottomRight, neighbour_bottom, neighbor_bottomLeft]
                newedge = [edge_left,edge_topLeft,edge_top,edge_topRight,
                           edge_right, edge_bottomRight, edge_bottom, edge_bottomLeft]   
                neighStr = str(n)+'||'+str(newneighbor)+'\n'        
                file2.write(neighStr)         
                file2.close()
                self.neighbor.append(newneighbor)
                self.edge.append(newedge)
                #end if
            i +=1

        #end while
        print ("i", i)
        print ("n",n)

        self.no_of_nodes = n
        
        for rowno in range(n):
            
                
            curr_node_r = self.node[rowno][1]
            curr_node_c = self.node[rowno][2]
            for order in range(8):           
                
                if self.neighbor[rowno][order] == 1:
                    
                    if order == 0:
                        neighbor_r = curr_node_r
                        neighbor_c = curr_node_c -1
        
                    elif order == 1:
                        neighbor_r = curr_node_r -1
                        neighbor_c = curr_node_c -1
       
                    elif order == 2:
                        neighbor_r = curr_node_r -1
                        neighbor_c = curr_node_c 
        
                    elif order == 3:
                        neighbor_r = curr_node_r -1
                        neighbor_c = curr_node_c +1
        
                    elif order == 4:
                        neighbor_r = curr_node_r
                        neighbor_c = curr_node_c +1 
        
                    elif order == 5:
                        neighbor_r = curr_node_r +1
                        neighbor_c = curr_node_c +1 
        
                    elif order == 6:
                        neighbor_r = curr_node_r +1
                        neighbor_c = curr_node_c 
        
                    elif order == 7:
                        neighbor_r = curr_node_r +1
                        neighbor_c = curr_node_c -1
        
                    #end if
                    
                    for (i,row) in enumerate(self.node):
                        #print ("i", i)
                        if (self.node[i][1] == neighbor_r) and (self.node[i][2] == neighbor_c):
                                                       
                            self.neighbor_node_no[rowno+1][order+1] = self.node[i][0]
                            
                        
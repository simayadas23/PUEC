# -*- coding: utf-8 -*-

"""
Created on Wed Nov 22 12:26:22 2017

@author: pragna
"""
import sys
sys.path.insert(0,'/home/pragna/rdflib')
import os
from rdflib import RDF, RDFS, Graph, Literal, Namespace#, URIRef, ConjunctiveGraph
#from rdflib import Literal#, URIRef
#from rdflib.namespace import XSD
from rdflib.plugins.sparql import prepareQuery
from collections import defaultdict
#import time
class newTT():
    def __init__(self,AGVno,rootDic):
        self.qresOther = defaultdict(dict)
        self.dirName = rootDic
        self.baseN = 'AGVont'
        self.suffix = '.owl'
        self.g = Graph()
        
        self.xsdNS = Namespace("http://www.w3.org/2001/XMLSchema#")
        self.xsdFloat = self.xsdNS["float"]
        self.owlNS = Namespace("http://www.w3.org/2002/07/owl#") 
        self.costNS = Namespace("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#")
        self.objPropNS = self.owlNS["ObjectProperty"]
        self.dataPropNS = self.owlNS["DatatypeProperty"]
        self.nodeClass = self.costNS["Node"]
        self.timeStampNS = self.costNS["timeStamp"]
        self.ttClass = self.costNS['travelTime']
        self.ontFile = ''
    def parseOnt(self,AGVno):
        
        self.ontfile = os.path.join(self.dirName, self.baseN + str(AGVno) + self.suffix)
        print('Parsing ont of AGV', AGVno)
        self.g.parse(self.ontfile, format="nt")
        self.g.commit()
    def serializeOnt(self, AGVno):
        print('Serializing ont of AGV', AGVno)
        self.g.serialize(destination=self.ontfile, format='nt')
        
        self.g.commit()
        
    def addNewTT(self, regNo, origin, destination,k,itr,X,AGVno):
        
        edgeClass = self.costNS["Edge"]
        strEdg = "edge-"+str(itr)
        invEdgNS = self.costNS[strEdg]
        self.g.add((invEdgNS, RDF.type, edgeClass))
        
        #create orgClass prop
        orgClass = self.costNS['origin']
        self.g.add((orgClass, RDF.type, self.objPropNS))
        self.g.add((orgClass, RDFS.domain, edgeClass))
        self.g.add((orgClass, RDFS.range, self.nodeClass))

        #give edge indv 'origin' property
        self.g.add((edgeClass, self.objPropNS, orgClass))
        strOrg = "node-"+str(origin)
        orgIndNS = self.costNS[strOrg]
        self.g.add((invEdgNS, orgClass, orgIndNS))

        #create "dest" objprop
        destClass = self.costNS['destination']
        self.g.add((destClass, RDF.type, self.objPropNS))
        self.g.add((destClass, RDFS.domain, edgeClass))
        self.g.add((destClass, RDFS.range, self.nodeClass))
        #give edge indv 'destination' property

        self.g.add((edgeClass, self.objPropNS, destClass))
        strDest = "node-"+str(destination)
        desIndNS = self.costNS[strDest]
        self.g.add((invEdgNS, destClass, desIndNS))

        #create each edge individual "tt" property 

        self.g.add((self.ttClass, RDF.type, self.dataPropNS))
        self.g.add((self.ttClass, RDFS.domain, edgeClass))
        self.g.add((self.ttClass, RDFS.range, self.xsdFloat))
        self.g.add((invEdgNS, self.ttClass, Literal(X, datatype=self.xsdFloat)))


        #give tt the 'timestamp' property
        #timeStampNS = costNS["timeStamp"]
        self.g.add((self.timeStampNS, RDF.type, self.dataPropNS))
        self.g.add((self.timeStampNS, RDFS.domain, edgeClass))
        self.g.add((self.timeStampNS, RDFS.range, self.xsdFloat))
        self.g.add((invEdgNS, self.timeStampNS, Literal(k, datatype=self.xsdFloat)))
              
        
        
    def fetchOtherObs(self,AGVno,orig,dest,rootDic,ontObjList):
        
        strOrg = "node-"+str(orig)
        strDest = "node-"+str(dest)
        origin= self.costNS[strOrg]#URIRef("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#node-"+str_curr_u)
        destination = self.costNS[strDest]#URIRef("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#node-"+str_neighbor)
        str2= ("""
        PREFIX ns: <http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?mCost ?k
        WHERE { 
               ?edge rdf:type ns:Edge;
                 ns:origin ?org .
               ?edge rdf:type ns:Edge;
                 ns:destination ?dest . 
               ?edge ns:travelTime ?mCost .
               ?edge ns:timeStamp ?k .
         }""")
        finalquery =  prepareQuery(str2)

        count = 1
        for i in range(0, len(ontObjList)):
            if (i !=(AGVno-1)):                          
                qres2 = ontObjList[i].g.query(finalquery, initBindings={'org': origin, 'dest':destination})#, initBindings={'org': origin, 'dest':destination})                t2=time.clock()
                if (len(qres2)!=0):
                    print("Observation found in other AGV(s) for the set of nodes")
                    self.qresOther[count] = qres2
                    count = count +1
                #end if
            #end if
        #end for
    

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
        #< http: // www.semanticweb.org / hilaire / ontologies / 2016 / 4 / untitled - ontology - 87  # >
        self.costNS = Namespace("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#")
        self.objPropNS = self.owlNS["ObjectProperty"]
        self.dataPropNS = self.owlNS["DatatypeProperty"]
        self.nodeClass = self.costNS["Node"]
        #self.timeStampNS = self.costNS["timeStamp"]
        #self.
        self.ontFile = os.path.join(self.dirName, self.baseN + str(AGVno) + self.suffix)

    def parseOnt(self,AGVno):
        
        self.ontfile = os.path.join(self.dirName, self.baseN + str(AGVno) + self.suffix)
        print('Parsing ont of AGV', AGVno)
        self.g.parse(self.ontfile, format="nt")
        self.g.commit()
    def serializeOnt(self, AGVno, format = 'nt'):
        print('Serializing ont of AGV', AGVno)
        self.g.serialize(destination=self.ontFile, format=format)
        
        self.g.commit()
        
    def addNewTT(self, origin, destination,k,
                 itr, X):
            edgeClass = self.costNS["Edge"]
            strEdg = "edge-" + str(itr)
            invEdgNS = self.costNS[strEdg]
            self.g.add((invEdgNS, RDF.type, edgeClass))

            # create "org" objprop
            orgClass = self.costNS['origin']
            self.g.add((orgClass, RDF.type, self.objPropNS))
            self.g.add((orgClass, RDFS.domain, edgeClass))
            self.g.add((orgClass, RDFS.range, self.nodeClass))

            # give edge indv 'origin' property
            self.g.add((edgeClass, self.objPropNS, orgClass))
            strOrg = "node-" + str(origin)
            orgIndNS = self.costNS[strOrg]
            self.g.add((invEdgNS, orgClass, orgIndNS))

            # create "dest" objprop
            destClass = self.costNS['destination']
            self.g.add((destClass, RDF.type, self.objPropNS))
            self.g.add((destClass, RDFS.domain, edgeClass))
            self.g.add((destClass, RDFS.range, self.nodeClass))

            # give edge indv 'destination' property
            self.g.add((edgeClass, self.objPropNS, destClass))
            strDest = "node-" + str(destination)
            desIndNS = self.costNS[strDest]
            self.g.add((invEdgNS, destClass, desIndNS))

            # create "timestamp" dataprop
            timeClass = self.costNS["timeStamp"]
            self.g.add((timeClass, RDF.type, self.dataPropNS))
            self.g.add((timeClass, RDFS.domain, edgeClass))
            self.g.add((timeClass, RDFS.range, self.xsdFloat))

            # give edge indv 'timestamp' property
            self.g.add((edgeClass, self.dataPropNS, timeClass))
            k = Literal(k, lang="foo")
            #timeStampIndNS = self.costNS[k]
            self.g.add((invEdgNS, timeClass, k))

            # create "traveltime" dataprop
            ttClass = self.costNS['travelTime']
            self.g.add((ttClass, RDF.type, self.dataPropNS))
            self.g.add((ttClass, RDFS.domain, edgeClass))
            self.g.add((ttClass, RDFS.range, self.xsdFloat))

            # give edge indv 'tt' property
            self.g.add((edgeClass, self.dataPropNS, ttClass))
            tt = Literal(X, lang="foo")
            #ttIndNS = self.costNS[tt]
            self.g.add((invEdgNS, ttClass, tt))
              
        
        
    def fetchOtherObs(self, AGVno, orig, dest, k):
        self.parseOnt(AGVno)
        strOrg = "node-"+str(orig)
        strDest = "node-"+str(dest)
        origin= self.costNS[strOrg]#URIRef("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#node-"+str_curr_u)
        destination = self.costNS[strDest]
        k = Literal(k, lang="foo")
        #timeStamp = self.costNS[k]
        #timeStamp = Literal(k, lang="foo")#URIRef("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#node-"+str_neighbor)
        str2= ("""
        PREFIX ns: <http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?mCost ?k
        WHERE { 
                ?edge rdf:type ns:Edge;
                    ns:origin ?org .
                ?edge rdf:type ns:Edge;
                    ns:destination ?dest .
                ?edge rdf:type ns:Edge;
                    ns:timeStamp ?k .
                ?edge rdf:type ns:Edge;
                    ns:travelTime ?mCost .
         }""")
        finalquery =  prepareQuery(str2)

        count = 0

        qres2 = self.g.query(finalquery, initBindings={'org': origin, 'dest':destination, 'k': k})#, initBindings={'org': origin, 'dest':destination})                t2=time.clock()
        for row in qres2:
            print("%s %s" % row)
        # if (len(qres2)!=0):
        #     print("Observation found in other AGV(s) for the set of nodes")
        #     count = count +1
        # print("Count", count)
                #end if
            #end if
        #end for
    
if __name__ == "__main__":
    c = 1
    rootDic = sys.argv[1]
    ontObj = newTT(c, rootDic)
    currNode = 245
    currNeighbor = 225
    tRegd = 5
    X_teqd = 7.90
    itr = 1

    ontObj.addNewTT(currNode, currNeighbor, tRegd, itr, X_teqd)
    s = ontObj.serializeOnt(c)
    ontObj.fetchOtherObs(c, 245, 225, 5)

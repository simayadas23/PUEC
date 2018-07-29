# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:26:22 2017

@author: pragna
"""
import sys
sys.path.insert(0,'/home/pragna/rdflib')
import os
from rdflib import OWL, RDF, RDFS, Graph, Namespace

def newOntCreate(AGVno, rootDic):
    g = Graph()
    dirName = rootDic
    baseN1 = 'AGVtestv3'
    suffix = '.owl'
    file1 = os.path.join(dirName, baseN1 + suffix)
    g.parse(file1, format="nt")


    xsdNS = Namespace("http://www.w3.org/2001/XMLSchema#")
    xsdFloat = xsdNS["float"]

    #define object classhttp://w
    owlNS = Namespace("http://www.w3.org/2002/07/owl#")
    costNS = Namespace("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#")
 
    #objectClass = costNS['Object']
    edgeClass = costNS["Edge"]
    nodeClass = costNS["Node"]
    ttClass = costNS['travelTime']
    timeStampNS = costNS["timeStamp"]
    orgClass = costNS['origin']
    destClass = costNS['destination']
    objPropNS = owlNS["ObjectProperty"]
    dataPropNS = owlNS["DatatypeProperty"]
   
    #create "edgeClass" as a OWl.Class
    g.add((edgeClass, RDF.type, OWL.Class))


    #create "tt" dataprop
    g.add((ttClass, RDF.type, dataPropNS))
    g.add((ttClass, RDFS.domain, edgeClass))
    g.add((ttClass, RDFS.range, xsdFloat))

    #create "timeStamp" dataprop
    g.add((timeStampNS, RDF.type, dataPropNS))
    g.add((timeStampNS, RDFS.domain, edgeClass))
    g.add((timeStampNS, RDFS.range, xsdFloat))

    #create "origin" objprop
    g.add((orgClass, RDF.type, objPropNS))
    g.add((orgClass, RDFS.domain, edgeClass))
    g.add((orgClass, RDFS.range, nodeClass))

    #create "dest" objprop
    g.add((destClass, RDF.type, objPropNS))
    g.add((destClass, RDFS.domain, edgeClass))
    g.add((destClass, RDFS.range, nodeClass))

   
    baseN2 = 'AGVont' 
    no = str(AGVno)
    file2 = os.path.join(dirName,baseN2 + no + suffix)
    #print(filename)
    g.serialize(destination=file2, format='nt')


    g.commit()
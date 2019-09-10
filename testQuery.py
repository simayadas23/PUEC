def fetchOtherObs(self, AGVno, orig, dest, rootDic, ontObjList):
    strOrg = "node-" + str(orig)
    strDest = "node-" + str(dest)
    origin = self.costNS[
        strOrg]  # URIRef("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#node-"+str_curr_u)
    destination = self.costNS[
        strDest]  # URIRef("http://www.semanticweb.org/hilaire/ontologies/2016/4/untitled-ontology-87#node-"+str_neighbor)
    str2 = ("""
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
    finalquery = prepareQuery(str2)

    count = 1
    for i in range(0, len(ontObjList)):
        if (i != (AGVno - 1)):
            qres2 = ontObjList[i].g.query(finalquery, initBindings={'org': origin,
                                                                    'dest': destination})  # , initBindings={'org': origin, 'dest':destination})                t2=time.clock()
            if (len(qres2) != 0):
                print("Observation found in other AGV(s) for the set of nodes")
                self.qresOther[count] = qres2
                count = count + 1
            # end if
        # end if
    # end for
if __name__ == "__main__":
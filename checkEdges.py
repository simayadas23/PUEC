import os
import numpy as np
import pandas as pd
i = 1
j = 0
totalCommonEdges = 0
#cntOneachCmb = 0
colN = 3
arrayCnt = []
arraySrc = []
arrayDst = []
agvF = []
agvS = []
lastCmb = ()
listLastCmb = []
listrevLastCmb = []
revlastCmb = ()
for i in range(1,5):
    print("looping", i)
    dir_name = '/home/pragna/Documents/PUEC'
    base_filename1 = 'Edges_u_d'
    suffix = '.txt'
    file_name1 = os.path.join(dir_name, base_filename1 + str(i) + suffix)
    print("Filename1", file_name1)
    f1 = np.loadtxt(file_name1)

    for j in range(1,5):
        if (j != i):
            cntOneachCmb = 0
            print("looping", j)
            file_name2 = os.path.join(dir_name, base_filename1 + str(j) + suffix)
            print("Filename2", file_name2)
            f2 = np.loadtxt(file_name2)
            currCmb = (i,j)
            if (currCmb not in listLastCmb and currCmb not in listrevLastCmb):
                    listrevLastCmb.clear()
                    print(i)
                    print(j)
                    lastCmb = (i,j)
                    listLastCmb.append(lastCmb)
                    print("listLastCmb", listLastCmb)

                    for h in range(0, len(listLastCmb)):
                        for k in reversed(listLastCmb[h]):
                            revlastCmb = revlastCmb + (k,)
                        listrevLastCmb.append(revlastCmb)
                        revlastCmb = ()
                    print("listrevLastCmb", listrevLastCmb)
                    for k in range(0, min(len(f1),len(f2))):
                        mapNoF = f1[k][0]
                        mapNoS = f2[k][0]
                        a = (f1[k][3], f1[k][4])
                        b = (f2[k][3], f2[k][4])

                        if (a == b and mapNoF == mapNoS): # and f1[k][3] == f2[k][3]) :
                    #print("Common Edge")
                            totalCommonEdges +=1
                            cntOneachCmb +=1


                            arrayCnt.append(totalCommonEdges)
                            arraySrc.append(f1[k][3])
                            arrayDst.append(f1[k][4])
                            agvF.append(i)
                            agvS.append(j)
            cmbCountDict = {currCmb: cntOneachCmb}
            print("cmbCountDict", cmbCountDict)

                #nd if
            #end for
        #end if
    #end for
#end for
#print(len(f1))
#print(len(f2))
print(len(arrayCnt))
print(len(arraySrc))
#print(arrayDst)
#print(agvF)
#print(agvS)
d1 = {'Count': arrayCnt}
d2 = {'SourceNode': arraySrc}
d3 = {'DestNode': arrayDst}
d4 = {'FirstAGV': agvF}
d5 = {'SecondAGV': agvS}
df1 = pd.DataFrame(data=d1)
df2 = pd.DataFrame(data=d2)
df3 = pd.DataFrame(data=d3)
df4 = pd.DataFrame(data=d4)
df5 = pd.DataFrame(data=d5)
writer = pd.ExcelWriter('/home/pragna/Documents/PUEC/Results.xlsx', engine='xlsxwriter')
workbook=writer.book
worksheet=workbook.add_worksheet('CommonEdges')
writer.sheets['CommonEdges'] = worksheet
#df_list = [df1,df2,df3, df4, df5]

# df1.to_excel(writer, sheet_name='CommonEdges')
# df2.to_excel(writer, sheet_name='CommonEdges')
# df3.to_excel(writer, sheet_name='CommonEdges')
# df4.to_excel(writer, sheet_name='CommonEdges')
# df5.to_excel(writer, sheet_name='CommonEdges')
#row = 0
#spaces = 1
#for dataframe in df_list:
new_df = pd.concat([df1, df2, df3, df4, df5], axis=1)
new_df.to_excel(writer,sheet_name='CommonEdges',startrow=0 , startcol=0)
    #row = row + len(dataframe.index) + spaces + 1
#end for
writer.save()










import os
import numpy as np
import pandas as pd
i = 1
j = 0
cnt = 0
colN = 3
arrayCnt = []
arraySrc = []
arrayDst = []
agvF = []
agvS = []
for i in range(1,5):
    dir_name = '/home/pragna/Documents/PUEC'
    base_filename1 = 'Edges_u_d'
    suffix = '.txt'
    file_name1 = os.path.join(dir_name, base_filename1 + str(i) + suffix)
    f1 = np.loadtxt(file_name1)
    for j in range(i-1,5):
        if (j != 0 and j != i):
            file_name2 = os.path.join(dir_name, base_filename1 + str(j) + suffix)
            f2 = np.loadtxt(file_name2)
            #f1 = np.loadtxt(file_name1)
            for k in range(0, min(len(f1),len(f2))):
                #a = (f1[k][2], f1[k][3])
                #b = (f2[k][2], f2[k][3])
                if (f1[k][2] == f2[k][2] and f1[k][3] == f2[k][3]) :
                    #print("Common Edge")
                    cnt +=1
                    arrayCnt.append(cnt)
                    arraySrc.append(f1[k][2])
                    arrayDst.append(f1[k][3])
                    agvF.append(i)
                    agvS.append(j)
                #nd if
            #end for
        #end if
    #end for
#end for
print(cnt)
d1 = {'Count': arrayCnt}
d2 = {'SourceNode': arraySrc}
d3 = {'DestNode': arrayDst}
d4 = {'FirstAGV': agvF}
d5 = {'SecondAGV': agvS}
df1 = pd.DataFrame(data=d1)
df2 = pd.DataFrame(data=d2)
df3 = pd.DataFrame(data=d3)
df4 = pd.DataFrame(data=d4)
writer = pd.ExcelWriter('/home/pragna/Documents/PUEC/Results.xlsx', engine='xlsxwriter')
df1.to_excel(writer, sheet_name='CommonEdges')
df2.to_excel(writer, sheet_name='CommonEdges')
df3.to_excel(writer, sheet_name='CommonEdges')
df4.to_excel(writer, sheet_name='CommonEdges')











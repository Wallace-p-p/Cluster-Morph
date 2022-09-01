import csv
import numpy as np
import pickle
b=[]
with open('C:\\Users\\walla\\Desktop\\HOME OFFICE\\imagens\\exoTrain.csv', newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in file:
        a= row
        try:
            x = np.array(a)
            b.append(x.astype(float))
        except:
            a=0
c=[]
for i in range(50):
    c.append(b[i][0:50])
l=c
with open("static\\example.txt", 'wb') as fp:
     pickle.dump(l, fp)


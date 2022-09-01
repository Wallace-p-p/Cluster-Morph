a = [
    [0,1,2,1,0],
    [0,100,200,100,0],
    [5, 50, 95,50,5],
    [0,1,1,1,2],
    [0,10,10,10,20],
    [0,10,12,9,22],
    [40,20,10,20,40],
    [4,2,1,2,4]
]
import pickle
import matplotlib.pyplot as plt
for i in range(len(a)):
    plt.plot(a[i])
    plt.title('Curve '+str(i))
    plt.xlabel('time')
    plt.ylabel('Some measurements')
    plt.savefig('static//explanation//curve-'+str(i)+'-plot.png')
    plt.clf()
for i in range(len(a)):
    plt.plot(a[i])
plt.title('Curve-all')
plt.xlabel('time')
plt.ylabel('Some measurements')
plt.savefig('static//explanation//curve-all-plot.png')
plt.clf()

l=a
with open("static\\explanation.txt", 'wb') as fp:
    pickle.dump(l, fp)
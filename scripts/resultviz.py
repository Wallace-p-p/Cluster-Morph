import pickle
with open('static//explanation//explanation-info.txt', 'rb') as fp:
    info= pickle.load(fp)
    fp.close()
groups=[]
for i in range(5):
    gg=[]
    rai = (i+0.1)
    with open('static//explanation//explanation-'+str(rai)+'groups.txt', 'rb') as fp:
        g= pickle.load(fp)
        fp.close()
    gg.append(rai)
    gg.append(g)
    groups.append(gg)
print(info)
'''
import matplotlib.pyplot as plt
plt.plot(info[0], info[1])
plt.title('Quality measure x radius')
plt.xlabel('radius')
plt.ylabel('Qaulity measure')
plt.savefig('static//explanation//info-plot.png')
plt.clf()
print(groups)'''
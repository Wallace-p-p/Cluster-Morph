#let us begin by importing tools

import matplotlib.pyplot as plt
import numpy as np
from biosppy.signals.tools import normalize , distance_profile
import pickle
import os
import shutil

def clusterthis(data, title):
    #Welcome to the controll station, here you will be able to manipulate the data, values and bounds.
    if os.path.exists('static/'+title) == False:
        try:
            os.mkdir(os.path.join('static/', title))
        except:
            print('impossible to create folder')
    title = title
    database = data        #list of arrays, each array being a time series
    metric2 = 'euclidean'   #'euclidean' or 'pearson', the metric used to build the matrix of similarity between the selected subsequences, inside distance profile
    H= normalize(signal=database, ddof=1)
    database = H[0]

    #Clustering
    RadiusTimes10Start = 1       #acceptance threshold *10, value of distance between the most similar subsequence until the end of the acptance interval to start the clustering
    RadiusTimes10MaxPlus1 = 51   #acceptance threshold *10 + 1, end value
    RadiusTimes10Growth = 10      #acceptance threshold *10, growth rhythm


    #1 tabela de distancia entre motifs // distance between motifs table
    DistMotifs= []
    DMp=[]
    LM = database
    for i in range(len(LM)):
        for j in range(i+1,len(LM)):
            if(len(LM[i])<=len(LM[j])/2):                                                      #here we compare different size curves by sliding the shorter one into the bigest and saving the euclidean distance values
                eucli = distance_profile(query=LM[i], signal=LM[j], metric=metric2)
                eucli=eucli[0]
            elif(len(LM[i])/2>=len(LM[j])):
                eucli = distance_profile(query=LM[j], signal=LM[i], metric=metric2)
                eucli=eucli[0]
            else:                                                                              #the tool used can only calculate the euclidean distance if the bigger curve has at least duble the size, so when that is not the case, the biggest one is concatenated with itself and only the values that are from the originals ones are considered

                if(len(LM[i])>=len(LM[j])):
                    o=[]
                    o= np.concatenate((LM[i], LM[i]), axis=0)
                    eucli = distance_profile(query=LM[j], signal=o, metric=metric2)
                    eucli= eucli[0]
                    a=[]
                    for b in range(len(LM[i])-len(LM[j])+1):
                        a.append(eucli[b])
                    eucli= a
                elif(len(LM[i])<len(LM[j])):
                    o=[]
                    o= np.concatenate((LM[j], LM[j]), axis=0)
                    eucli = distance_profile(query=LM[i], signal=o, metric=metric2)
                    eucli= eucli[0]
                    a=[]
                    for b in range(len(LM[j])-len(LM[i])+1):
                        a.append(eucli[b])
                    eucli= a

            DMp.append(np.min(eucli))
        DistMotifs.append(DMp)                                                           #DistMotifs has the minimal distance value from the comparison between each curve in ListMotifs 
        DMp= []
    #save as txt distmotifs - distance between each curve
    l=DistMotifs
    with open('static//'+title+'//'+title+"-distance-between-curves.txt", 'wb') as fp:
        pickle.dump(l, fp)
        fp.close()
    #2 Agrupamento - variando o raio para o agrupamento, guardando raio e medida de qualidade / clustering - varying radius for clusters, keeping radius and quality measure
    ra=[]
    medidaqualidade= []
    informacao=[]
    for rai in range(RadiusTimes10Start, RadiusTimes10MaxPlus1, RadiusTimes10Growth):
        with open('static//'+title+'//'+title+"-distance-between-curves.txt", 'rb') as fp:
            D= pickle.load(fp)                                     #D = DistMotifs
            fp.close()                                           
        raio= rai/10                                            #radius/10
        # agrupando motifs / clustering motifs
        g=[]
        for a in range(len(D)):
            gg=[]
            c= a
            h=0
            for u in range(len(g)):
                if c not in (g[u]):
                    h=h+1
            if(h==len(g)):
                if D[a] != []:
                    gg.append(a)
                    for jun in range(len(D[a])):     #armazena todos os possiveis casos em que a curva se repitiu
                        if(D[a][jun]<=raio):
                            c= a + jun +1
                            h=0
                            for u in range(len(g)):
                                if c not in (g[u]):
                                    h= h + 1
                            if(h==len(g)):
                                gg.append(c)
                    
                    g.append(gg)                                            #g contains all the separations of groups, being a list of arrays where each array is a group and each element is the index -1 of a curve in the ListMotif
        #salva o agrupamento
        l=g
        with open('static//'+title+'//'+title+'-'+str(raio)+"groups.txt", 'wb') as fp:
            pickle.dump(l, fp)
            fp.close()

        #3 Qualidade do agrupamento  / quality of the cluster process
        #comparação de distancias intra grupo / intra cluster distance comparation
        with open('static//'+title+'//'+title+"-distance-between-curves.txt", 'rb') as fp:
            D= pickle.load(fp)
            fp.close()
        DistMotifs=D
        o=[]
        gg= []
        for f in range(len(g)):                                                         #deleta todos os grupos com menos de 2 integrantes / deletes all groups with less than 2 elements
            if(len(g[f])<2):
                gg.append(f)
        for f in range(len (gg) - 1, -1, -1):
            del(g[gg[f]])
        if(len(g)==0):                                                                 #if there is no group with more than 1 component, continues to next value of for
            continue

        for u in range(len(g)):
            i=[]
            for v in range(len(g[u])):
                j=[]                                                                     #j contains the distance between each member of the group
                for l in range(len(g[u])):
                    if(g[u][v]!=g[u][l]):
                        if(g[u][v]<g[u][l]):
                            j.append(DistMotifs[g[u][v]][g[u][l]- g[u][v] - 1])
                        else:
                            j.append(DistMotifs[g[u][l]][g[u][v]- g[u][l] - 1])
                a=0
                for n in range(len(j)):
                    a= a + j[n]
                a= a/len(j)                                                              
                i.append(a)
            o.append(i)                                                                 #o contains the means of the distances of each member compared to all the others members of the group
        medg=[]
        centroides=[]
        for r in range(len(o)):
            centroides.append(np.argmin(o[r]))                                          #centroides contains the index of the member most similar to all others in the group 
            medg.append(np.min(o[r]))
        me=0
        for r in range(len(medg)):
            me= me + medg[r]
        
        valorintra= me/len(o)                                                           #valorintra contains the mean of the minimal mean distante inside each group
    
        #comparação de distâncias extra grupos  / clusters distance comparation
        centros=[]
        i=[]
        for l in range(len(centroides)):                                                #centro contains the index of the representative of each group
            centros.append(g[l][centroides[l]])
        a=0
        for v in range(len(centros)):
            j=[]
            for l in range(len(centros)):
                if(centros[v]!=centros[l]):
                    if(centros[v]<centros[l]):
                        j.append(DistMotifs[centros[v]][centros[l]- centros[v] - 1])
                    else:
                        j.append(DistMotifs[centros[l]][centros[v]- centros[l] - 1])

            a= min(j)                                                                 #a contains the distance to the representative of the group with the most similar representative of other group
            i.append(a)
        aa=0
        for n in range(len(i)):
            aa= aa + i[n]
        
        valorextra= aa/len(i)                                                         #valorextra contains the mean of the minimal distances of the closest representatives
        

        #medida de qualidade / quality measure
        mq= (valorextra - valorintra)/max(valorintra, valorextra)
        ra.append(raio)
        medidaqualidade.append(mq)                                                   #medida de qualidade contains the qualite measure adopted of the clustering
        
        #salva os representantes
        Representatives=[]
        for nrepresentatives in range(len(centros)):
            Representatives.append(LM[centros[nrepresentatives] + 1])
        with open('static//'+title+'//'+str(raio) + "representants"+".txt", 'wb') as fp:
            pickle.dump(Representatives, fp)
            fp.close()
            

    informacao.append(ra)
    informacao.append(medidaqualidade)
    with open('static//'+title+'//'+title+"-info.txt", 'wb') as fp:                                         #informacao contains each radius size and the compatible quality measure of the clustering
        pickle.dump(informacao, fp)
        fp.close()
    import matplotlib.pyplot as plt
    plt.plot(informacao[0], informacao[1])
    plt.title('Quality measure x radius')
    plt.xlabel('radius')
    plt.ylabel('Qaulity measure')
    plt.savefig('static//'+title+'//'+title+"-info-plot.png")
    plt.clf()
    plt.close('all')
    shutil.make_archive('static//'+title+'//'+'results', 'gztar', 'static/'+title)
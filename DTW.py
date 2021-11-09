from python_speech_features import mfcc
import math
from scipy.io.wavfile import read
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import numpy as np
import matplotlib.pyplot as plt


def distance(element_audio1,element_audio2):
    sum=0
    for i in range(element_audio1.size):
        sum=sum+pow(element_audio1[i] - element_audio2[i] , 2)
    return math.sqrt( sum ) 

def DTW (audio1, audio2):

    matrice_distance=-np.ones((len(audio1),len(audio2)))

    alignement_Dis= []
    empty_alignement_Dis = (None,None)
    for i in range(len(audio1)):
        row= []
        for j in range(len(audio2)):
            row.append(empty_alignement_Dis)
        alignement_Dis.append(row)

    for i in range(len(audio1)):
        for j in range(len(audio2)):

            if (i == 0) and (j == 0):
                matrice_distance[i][j] = distance(audio1[i],audio2[j])
                alignement_Dis[i][j] = (None,None)
                
            elif (i == 0):
                matrice_distance[i][j]= matrice_distance[i][j-1] + distance(audio1[i],audio2[j]) 
                alignement_Dis[i][j] = (i,j-1)

            elif (j == 0):
                matrice_distance[i][j]= matrice_distance[i-1][j] + distance(audio1[i],audio2[j]) 
                alignement_Dis[i][j] = (i-1,j)

            else:

                lowest_matrice_distance = matrice_distance[i-1][j]
                alignement_Dis[i][j] = (i-1,j)

                if matrice_distance[i][j-1] < lowest_matrice_distance:
                    lowest_matrice_distance = matrice_distance[i][j-1]
                    alignement_Dis[i][j] = (i,j-1)

                if matrice_distance[i-1][j-1] < lowest_matrice_distance:
                    lowest_matrice_distance = matrice_distance[i-1][j-1]
                    alignement_Dis[i][j] = (i-1,j-1)
                
                matrice_distance[i][j] = lowest_matrice_distance + distance(audio1[i],audio2[j])
    
    alignement=[]
    i,j = len(audio1)-1 , len(audio2)-1
    alignement.append( (i,j) )
    while ( (i!=0) or (j!=0) ):
        alignement.append(alignement_Dis[i][j])
        i,j = alignement_Dis[i][j]
    alignement.reverse()
    D = matrice_distance[len(audio1)-1][len(audio2)-1]

    return D,alignement

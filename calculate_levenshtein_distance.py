from Levenshtein import distance
import numpy as np
from time import time

def get_distance_matrix(str_list1, str_list2):
    """ Construct a levenshtein distance matrix for a list of strings"""
    dist_matrix = np.zeros(shape=(len(str_list1), len(str_list2)))
    t0 = time()
    print("Starting to build distance matrix. This will iterate from 0 till ", len(str_list1)) 
    for i in range(0, len(str_list1)):
        for j in range(0, len(str_list2)):
                dist_matrix[i][j] = distance(str_list1[i], str_list2[j])
                dist_matrix[j][i] = distance(str_list1[j], str_list2[i])
    t1 = time()
    print("took", (t1-t0), "seconds")
    # sum of each rows minimum of dist_matrix
    return(dist_matrix)
    

#str_list = ["analyze", "analyse", "analysis", "analyst", "analyze"]

#ggl_list = ['ios','windows','apple emojis','ios marktanteil','ios security','ios emojis','chrome os','iphone meme','apple meme','apple']
#ccr_list = ['apple', 'piccolo', 'windows', 'blackberry', 'player', 'chrome', 'mac', 'bb', 'amazon', 'limo']

#get_distance_matrix(ggl_list, ccr_list)


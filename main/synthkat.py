import gensim
from gensim import corpora, models, similarities
import csv
import os
import sqlite3
import numpy
import scipy
from scipy.cluster.hierarchy import ward, dendrogram, fcluster
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import scipy.special as special
import matplotlib.pyplot as plt

#csv files as input / sql query. label in col1 and text description in col2
vessels = ##either csv or sql query

#make txt files for gensim
with open('vessels.txt', 'w') as file:
    for i in range(len(vessels)):
        file.write(''.join(vessles[i][1])+'\n')

files = ['vessels.txt']

for i in range(len(vessels)):
    labels = labels + [vessels[i][0]]

for filename in files:
    class MyCorpus(object):
        def __iter__(self):
            for line in open(filename):
                yield dictionary.doc2bow(line.lower().split())

    dictionary = corpora.Dictionary(line.lower().split() for line in open(filename))
    dictionary.compactify()

    corpus = MyCorpus()
    print('Corpus finished.')

    X1 = gensim.matutils.corpus2dense(corpus,num_terms=len(dictionary))
    X = numpy.transpose(X1)

## Alternative distance measure: Jaccard index
##    jaccardmat = pdist(X, 'jaccard')
##    print("Jaccard distance finished.\n")

    cosmat1 = pdist(X, 'cosine')
    cosmat = squareform(cosmat1)
    print("Cosine distances finished.\n")

    wmat = ward(cosmat)
    max_d = 30 #Lower distance makes manual combination easier
    kats_n = fcluster(wmat,  max_d, criterion='distance')
    kats = []
    for i in range(len(kats_n)):
        kats = kats + [kats_n[i].item()]
    print("Creating KATS {0}".format(filename))

#save back to csv / reinsert values into sql database for manual checking

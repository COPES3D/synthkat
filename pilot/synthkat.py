import gensim
from gensim import corpora, models, similarities
import csv
import numpy
import scipy
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt

def jaccard(a,b):
    return float(len(set.intersection(*[set(a), set(b)])))/float(len(set.union(*[set(a), set(b)])))
    
#fancy_dendrogram from https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)
    ddata = dendrogram(*args, **kwargs)
    if not kwargs.get('no_plot', False):
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

#Enter data as txt files. See datascrub.py for initial processing of csv files.

files = ['pilot-ware.txt','pilotform.txt']

#Create list of titles from processed csv version.
titles = []
with open('pilot-ware.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
       titles = titles + [line]

#Distance matrices
print("Starting to calculate distance matrices.\n")
for filename in files:
    class MyCorpus(object):
        def __iter__(self):
            for line in open(filename):
                yield dictionary.doc2bow(line.lower().split())

    dictionary = corpora.Dictionary(line.lower().split() for line in open(filename))
    dictionary.compactify()

    #export dictionary to csv
    with open('{}-dictionary.csv'.format(filename),'w', newline ='') as file:
        w = csv.writer(file)
        w.writerows(dictionary.token2id.items())

    corpus = MyCorpus()

    #create matrix of jaccard values
    with open('{}-jaccard.csv'.format(filename), 'w', newline='') as file:
        writer = csv.writer(file)
        for i in corpus:
            jrow = []
            for j in corpus:
                jrow = jrow + [jaccard(i,j)]
            writer.writerow(jrow)

    c = 0
    for i in corpus:
        c = c + 1

    #Create distance matrix based on cosine similarity
    print("Starting cosine similarities...\n")
    cosmat = numpy.zeros([c,c])
    ci = 0
    for i in corpus:
        cj = 0
        for j in corpus:
            cosmat[ci,cj] = gensim.matutils.cossim(i,j)
            cj = cj + 1
        ci = ci + 1
    with open('{}-cosinesim.csv'.format(filename),'w', newline ='') as file:
        w = csv.writer(file)
        for row in cosmat:
            w.writerow(row)
    print("Cosine similarities finished.\n")

    #Change similarities to distances
    dist = numpy.genfromtxt('{}-cosinesim.csv'.format(filename), delimiter = ',')
    x = numpy.zeros_like(dist)
    for i in range(len(dist)):
        for j in range(len(dist)):
            x[i,j] = 1 - dist[i,j]

    distmethod = ['cosinesim','jaccard']

    for method in distmethod:
        #Change similarities to distances
        dist = numpy.genfromtxt('{0}-{1}.csv'.format(filename,method), delimiter = ',')
        x = numpy.zeros_like(dist)
        for i in range(len(dist)):
            for j in range(len(dist)):
                x[i,j] = 1 - dist[i,j]

        #Start cluster analysis
        wmat = ward(x)

        max_d = 10

        fancy_dendrogram(
            wmat,
            truncate_mode='lastp',
            p = 200,
            leaf_rotation= 90.,
            leaf_font_size=12.,
            show_contracted = True,
            annotate_above=2,
            max_d=max_d,
            )

        plt.savefig('{}-{}-clusters.png'.format(filename,method), dpi=200) #save figure as ward_clusters
        plt.clf()

        kats = fcluster(wmat,  max_d, criterion='distance')
        print("Creating KATS {0} - {1}".format(filename,method))
        with open('kats-{0}-{1}.csv'.format(filename,method), 'w', newline='') as file:
            writer = csv.writer(file)
            for row in sorted(zip(kats,titles)):
                writer.writerow(row)

#Results will appear as .csv list of kat numbers

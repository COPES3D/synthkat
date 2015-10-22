#from gensim import corpora, models, similarities
import gensim
import csv
import numpy
import scipy

def jaccard(a,b):
    return float(len(set.intersection(*[set(a), set(b)]))/float(len(set.union(*[set(a), set(b)])))

#from txt to corpus
class MyCorpus(object):
    def __iter__(self):
        for line in open('object.txt'):
            yield dictionary.doc2bow(line.lower().split())

dictionary = corpora.Dictionary(line.lower().split() for line in open('object2.txt'))
dictionary.compactify()

#export a reference dictionary to csv
with open('dictionary.csv','w', newline ='') as file:
    w = csv.writer(file)
    w.writerows(dictionary.token2id.items())
corpus_memory_friendly = MyCorpus()

with open('jaccard.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in corpus_memory_friendly:
        jrow = []
        for j in corpus_memory_friendly:
            jrow = jrow + [jaccard(i,j)]
        writer.writerow(jrow)

mat = numpy.genfromtxt("jaccard.csv", delimiter=",")

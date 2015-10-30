from gensim import corpora, models, similarities
import csv
import numpy
import scipy
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import json

def jaccard(a,b):
    return float(len(set.intersection(*[set(a), set(b)])))/float(len(set.union(*[set(a), set(b)])))

#Scrub preliminary csv data 

addrelform = []
addrelware = []

with open('addrelform.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        while line.count("") > 0:
            line.remove("")
        addrelform = addrelform + [line]
with open('addrelware.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        while line.count("") > 0:
            line.remove("")
        addrelware = addrelware + [line]

a = [] #ware
b = [] #form

with open('prelim-ware.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        while line.count("") > 0:
            line.remove("")
        for i in line:
            for j in addrelware:
                if i == j[0]:
                    for k in j[1:]:
                        if k not in line:
                            line = line + [k]
        a = a + [line]

with open('prelim-form.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        while line.count("") > 0:
            line.remove("")
        for i in line:
            for j in addrelform:
                if i == j[0]:
                    for k in j[1:]:
                        if k not in line:
                            line = line + [k]
        b = b + [line]

#Filter out most typological ids from ware, Remove duplicates
types = ["Form","Group","tav","Morel","Lamboglia","Conspectus","Ricci","Marabini","Dyson","Mayet","Vegas","Hayes"]
for i in a:
    for j in i[1:]:
        for k in types:
            if k in j:
                i.remove(j)

#Remove duplicates
for i in a:
    for j in i:
        while i.count(j) > 1:
            i.remove(j)
for i in b:
    for j in i:
        while i.count(j) > 1:
            i.remove(j)

#Make a json version
with open('synthkatdata.json', 'w') as file:
    file.write('{data:{\n')
    #file.write('{\n')
    for row in b:
        file.write('"'+row[0]+'": {\n')
        file.write('    "form":[')
        for i in range(len(row[1:])):
            file.write('"' + row[i + 1] + '"')
            if i + 1 != len(row[1:]):
                file.write(',')
        file.write('],\n')
        file.write('    "ware":[')
        for i in range(len(a[b.index(row)][1:])):
            file.write('"' + a[b.index(row)][i + 1] + '"')
            if i + 1 != len(a[b.index(row)][1:]):
                file.write(',')
        file.write(']\n')
        if b.index(row) != len(b):
            file.write('    },\n')
        if b.index(row) == len(b):
            file.write('    }\n')
    file.write('}\n}\n')

#Make csv versions
with open('byware.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    for row in a:
        writer.writerow(row)
with open('byform.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    for row in b:
        writer.writerow(row)

#Make a list of labels
titles = []
for i in range(len(b)):
    titles = titles + [b[i][0]]

#Make txt files
with open('byware.txt', 'w') as file:
    for i in a:
        file.write(' '.join(i)+'\n')
with open('byform.txt', 'w') as file:
    for i in b:
        file.write(' '.join(i)+'\n')

files = ['byware.txt','byform.txt']

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

    #corpus_memory_friendly = MyCorpus()
    corpus = MyCorpus()
    #corpora.MmCorpus.serialize('corpus.mm', corpus)

    #Perform tf-idf on the corpus
    #tfidf = models.TfidfModel(corpus)
    #corpus_tfidf = tfidf[corpus]
    #corpus = corpus_tfidf

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

    #Start cluster analysis
    wmat = ward(x)

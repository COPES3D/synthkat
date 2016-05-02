import csv
import numpy

a = [] #ware
b = [] #form

#Scrub raw entries in csv for both vessel ware and form to eliminate duplicate entries, filter out typological labels from vessel class ids.

with open('prelim-ware.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        while line.count("") > 0:
            line.remove("")
        a = a + [line]

with open('prelim-form.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        while line.count("") > 0:
            line.remove("")
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

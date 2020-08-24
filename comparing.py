#! /usr/bin/env python3

t = open('TfixedCorrs.txt')
f = open('fixedCorrs.txt')
r = open('FvsT.txt', 'w')

#compare Friday correlations with Tuesday correlations, output to FvsT file
T = {}
F = {}
for line in t.readlines():
    fields = line.strip().split("\t")
    T[fields[0]+fields[1]] = fields[2]
for line in f.readlines():
    fields = line.strip().split("\t")
    F[fields[0]+fields[1]] = fields[2]

r.write("Plaza\t\t\tFriday\t\tTuesday\t\tGreater\t\tHow Many Times Greater\n\n")

#for each plaza
for i in T:
    #If the Sunset vs Friday rush hour correlation is > the Sunset vs Tuesday rush hour correlation
    if(F[i]>T[i]):
        r.write(i + " \t" + F[i] + " \t" + T[i] + " \tFRIDAY  \t" + str(abs(float(F[i])/float(T[i]))) + "\n")
        #(use absolute value because we are just looking at strength of correlation, not whether the correlation
        #is negative or positive)
    else:
        r.write(i + " \t" + F[i] + " \t" + T[i] + " \tTuesday \t" + str(abs(float(T[i])/float(F[i]))) + "\n")
r.write("\n#We see that Friday correlations are generally greater that the Tuesday correlations,")
r.write("\n#and when the Tuesday correlations are greater, it is always a case in which both the\n")
r.write("#Friday correlation and the Tuesday correlation are small.\n")
r.close()

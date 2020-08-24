#! /usr/bin/env python3

import pandas as pd

r = open('results.txt', 'w')

#Rockaways are counted as separate from Queens because they are separated in                                                                                                             
#the MTA traffic data                                                                                                                                                                    
boroughs = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island", "Rockaways"]

#population of each borough in 2011                                                                                                                                                      
populations = [1400899, 2546662, 1611550, 2262013, 471564, 127400]

#Jewish population of each borough in 2011, from a 2011 Jewish Data Bank study                                                                                                           
#(I could not find up-to-date NYC population data for 7th Day Adventists,                                                                                                                
#so I am looking at Jewish populations as an estimate of Sabbath observant populations.)                                                                                                 
jewish = [5400, 561000, 240000, 198000, 34000, 22500]

#Jewish population weighted according to percent of Jewish children ages 15-17 who currently                                                                                            
#attend Jewish day school as an estimate of Orthodox (Sabbath observant) Jewish population.                   
#92% of NYC children aged 15-17 in day school are Orthodox (same study as above.)
#Rockaway uses the same percentage as Queens because it is in Queens.
dayschools = [5400*.55, 561000*.88, 240000*.38, 198000*.57, 34000*.27, 22500*.57]

#Jewish population weighted according to percent of Jewish households affiliated with a                                                                                                  
#congregation as another estimate of Sabbath observance (same study, same Rockaway approximation.)                                                                          
members = [5400*.29, 561000*.53, 240000*.32, 198000*.42, 34000*.41, 22500*.42]

#Jewish population as a percentage of total population for each borough                                                                                                                  
jpops = {}
for i in range(6):
    jpops[boroughs[i]] = jewish[i]/populations[i]
#Same, weighted by day school attendance                                       
dspops = {}
for i in range(6):
    dspops[boroughs[i]] = dayschools[i]/populations[i]
#Same, weighted according to congregation affiliation                                                                                                                 
mempops = {}
for i in range(6):
    mempops[boroughs[i]] = members[i]/populations[i]

#create pandas Series of correlations between sunset and rush hour traffic for each toll plaza and direction
f = open('fixedCorrs.txt').readlines()
correlations = []
plazas = []
counter = 0
for line in f:
    fields = line.split("\t")
    plazas.append([int(fields[0][5:]), 0])
    plazas[counter][1] = fields[1][:1]
    correlations.append(float(line.split("\t")[2][:-1]))
    counter += 1
s1 = pd.Series(correlations)

#create pandas Series of percentage of population that is Sabbath observant in each borough for each of the 3 estimates
g = open('plazakey').readlines()
destinations = {}
for line in g:
    fields = line.split("\t")
    destinations[fields[0]+fields[1]] = fields[2]
pops = [jpops[destinations[str(plazas[i][0])+plazas[i][1]]] for i in range(20)]
pops2 = [dspops[destinations[str(plazas[i][0])+plazas[i][1]]] for i in range(20)]
pops3 = [mempops[destinations[str(plazas[i][0])+plazas[i][1]]] for i in range(20)]
s2 = pd.Series(pops)
s3 = pd.Series(pops2)
s4 = pd.Series(pops3)

r.write("Correlation between Jewish population and correlation measure between Friday afternoon traffic and sunset times in NYC boroughs: ")
r.write(str(s1.corr(s2)) + "\n")
r.write("Same as above but for Sabbath-observant Jewish population only, using Jewish day school education as an estimate of Sabbath observance: ")
r.write(str(s1.corr(s3)) + "\n")
r.write("Same as above using congregation affiliation as an estimate of Sabbath observance: ")
r.write(str(s1.corr(s4)) + "\n")

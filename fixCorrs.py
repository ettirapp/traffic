#! /usr/bin/env python3

import re

#formatting correlation data for convenient viewing, removing extraneous text

#for Fridays, Fridays just outer boroughs, and Tuesdays:
for weekday in ["", "M", "T"]:
    f = open(weekday + 'correlations.txt').readlines()
    g = open(weekday + 'fixedCorrs.txt', 'w')
    temp = []
    for line in f:
        good = re.sub("dtype: float64", "", line)
        better = re.sub('\s+0\s+', '\t', good)
        betterer = re.sub(' ', '\t', better)
        betterest = re.sub('([0-9])([OI])', r'\1\t\2', betterer)
        temp.append(betterest)
    temp.sort()
    for line in temp:
        g.write(line)
    g.close()

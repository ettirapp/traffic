#! /usr/bin/env python3

import os

#combine the rush hours for all plazas into one file
for weekday in ["", "T"]:
    g = open(weekday + 'rushhours.txt', 'w')
    for plaza in os.listdir(weekday + 'sorted3'):
        for direction in os.listdir(weekday + 'sorted3/' + plaza):
            f = open(weekday + 'sorted3/' + plaza + "/" + direction + "/part-00000")
            line = f.readline()
            while(line):
                fields = line.split("\t")
                g.write(fields[1])
                line = f.readline()
            
            

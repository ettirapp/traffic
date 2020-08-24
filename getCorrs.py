#! /usr/bin/env python3

import datetime as dt
import pandas as pd
import matplotlib.dates as md
import os

#calculate Pearson correlation coefficients for the relationship between sunset times and afternoon
#traffic patterns for every bridge and tunnel in both directions for Fridays and Tuesdays.

for boroughs in [["", "friday"], ["M", "friday"], ["T", "tuesday"]]:
    answer = open(boroughs[0] + 'correlations.txt', 'w')

    #create a pandas DataFrame with sunset data
    f2 = open(boroughs[1] + 'Sunsets/part-00000')
    lines2 = f2.readlines()
    sundates = [line.split("\t")[0] for line in lines2]
    x2 = [md.date2num(dt.datetime.strptime(d, "%m/%d/%Y")) for d in sundates]
    suntimes = [line.split("\t")[1] for line in lines2]
    y2 = [md.date2num(dt.datetime(1900, 1, 1, int(str(t)[:-3]), int(str(t)[-3:]))) for t in suntimes]
    df2 = pd.DataFrame(y2, index=x2)

    #create a pandas DataFrame with traffic data for each toll plaza and traffic direction
    for plazadir in os.listdir(boroughs[0] + 'averaged'):
        f = open(boroughs[0] + 'averaged/' + plazadir + '/part-00000')
        lines = f.readlines()
        dates = [line.split("\t")[0] for line in lines]
        x = [md.date2num(dt.datetime.strptime(d, "%m/%d/%Y")) for d in dates]
        times = [line.split("\t")[1] for line in lines]
        y = [md.date2num(dt.datetime(1900, 1, 1) + dt.timedelta(hours = float(t))) for t in times]
        df = pd.DataFrame(y, index=x)

        #calculate correlation coefficient and write it to the proper file
        correlation = df.corrwith(df2)
        answer.write(plazadir + "\t" + str(correlation))

    answer.close()

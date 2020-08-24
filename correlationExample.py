#! /usr/bin/env python3

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

#This file creates a plot of sunset times, Friday traffic patterns, and Tuesday traffic patterns.                           
#This plot looks at plaza 5 (Marine Parkway - Gil Hodges Memorial Bridge) outbound (heading from the
#Rockaways to Brooklyn) which was chosen because of its high correlation between sunset and Friday afternoon                                                                        
#traffic. This plot shows that that Friday traffic varies in relation to sunset but Tuesday does not
#(at least not noticeably), indicating that Sabbath observance is causing the shift in traffic with sunset changes.

fig = plt.figure()

f = open('fridaySunsets/part-00000')
lines = f.readlines()
#formatting the sunset data as plottable dates and times               
sundates = [line.split("\t")[0] for line in lines]
x1 = [md.date2num(dt.datetime.strptime(d, "%m/%d/%Y")) for d in sundates]
suntimes = [line.split("\t")[1] for line in lines]
y1 = [md.date2num(dt.datetime(1900, 1, 1, int(str(t)[:-3]), int(str(t)[-3:]))) for t in suntimes]

f2 = open('averaged/plaza5OutboundPM/part-00000')
lines2 = f2.readlines()
#formatting the traffic data as plottable dates and times
dates = [line.split("\t")[0] for line in lines2]
x2 = [md.date2num(dt.datetime.strptime(d, "%m/%d/%Y")) for d in dates]
times = [line.split("\t")[1] for line in lines2]
#1900 chosen as a random date to ensure that all times would have a consistent date
y2 = [md.date2num(dt.datetime(1900, 1, 1) + dt.timedelta(hours = float(t))) for t in times]

#Use Friday sunset times as the axis even though Tuesday sunset times are slightly different because
#the shape of the plot will be almost exactly the same, it will just be slightly shifted.

f3 = open('Taveraged/plaza5OutboundPM/part-00000')
lines3 = f3.readlines()
#formatting the traffic data as plottable dates and times                           
dates = [line.split("\t")[0] for line in lines3]
x3 = [md.date2num(dt.datetime.strptime(d, "%m/%d/%Y")) for d in dates]
times = [line.split("\t")[1] for line in lines3]
#1900 chosen as a random date to ensure that all times would have a consistent date                                                             
y3 = [md.date2num(dt.datetime(1900, 1, 1) + dt.timedelta(hours = float(t))) for t in times]

plt.axis('off')
plt.title("Correlation Between Sunset and Friday PM Traffic")
ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True, sharey=False)
ax1.xaxis.set_major_locator(md.YearLocator())
ax1.xaxis.set_major_formatter(md.DateFormatter('%Y'))
ax1.yaxis.set_major_locator(md.HourLocator())
ax1.yaxis.set_major_formatter(md.DateFormatter('%H:%M'))
ax1.yaxis.set_minor_locator(md.MinuteLocator(30))
ax2.yaxis.set_major_locator(md.HourLocator())
ax2.yaxis.set_major_formatter(md.DateFormatter('%H:%M'))
ax2.yaxis.set_minor_locator(md.MinuteLocator(30))
ax2.yaxis.set_minor_formatter(md.DateFormatter('%H:%M'))
ax3.yaxis.set_major_locator(md.HourLocator())
ax3.yaxis.set_major_formatter(md.DateFormatter('%H:%M'))
ax3.yaxis.set_minor_locator(md.MinuteLocator(30))
ax3.yaxis.set_minor_formatter(md.DateFormatter('%H:%M'))
ax1.plot(x1, y1, 'b-', label="Sunset")
ax1.legend()
ax2.scatter(x2, y2, c='green', label="Friday Rush Hour")
ax2.legend()
ax2.set_ylim([md.date2num(dt.datetime(1900, 1, 1, 15, 45)), md.date2num(dt.datetime(1900, 1, 1, 16, 15))])
ax3.scatter(x3, y3, c='red', label="Tuesday Rush Hour")
ax3.legend()
ax3.set_ylim([md.date2num(dt.datetime(1900, 1, 1, 15, 45)), md.date2num(dt.datetime(1900, 1, 1, 16, 15))])
plt.xlabel("Date")
ax2.set_ylabel("Time")
plt.savefig("TandF.pdf")

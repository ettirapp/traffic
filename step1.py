#! /usr/bin/env python3

import pyspark
from datetime import datetime

def getFields(x):
    fields = x.split("\t")
    plaza = fields[0]
    date = fields[1]
    hour = fields[2]
    direction = fields[3]
    ezpass = fields[4]
    cash = fields[5]
    return (plaza, date, hour, direction, ezpass, cash)

#filter data by AM only or PM only, depending on what we're looking for
def AMorPM(x,y):
    if y[2] == "AM":
        return int(x[2]) < 12
    else:
        return int(x[2]) >= 12

#reassign plaza numbers so that toll plaza IDs for the same plaza for
#before and after Open Road Tolling switchover are the same (see MTAdictionary)
def mapPlazas(x):
    myDict = {21:1, 22:2, 23:3, 24:4, 25:5, 26:6, 27:7, 28:8, 29:9, 30:10, 11:10}
    newPlaza = x[0]
    if int(x[0]) in myDict:
        newPlaza = myDict[int(x[0])]
    return str(newPlaza) + "\t" + str(x[1]) + "\t" + str(x[2]) + "\t" + str(x[3])
    
sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

textFile = sc.textFile('MTAHourlyTraffic.tsv')

#sort data into separate folders for Inbound and Outbound, and filter out all AM data
for weekday in [[1, "T"], [4, ""]]:
    for i in [["I", "Inbound", "PM"], ["O", "Outbound", "PM"]]:
        a = textFile.map(getFields) \
                    .filter(lambda x: datetime.strptime(x[1], "%m/%d/%Y").weekday()==weekday[0]) \
                    .filter(lambda x: AMorPM(x, i)) \
                    .filter(lambda x: x[3] == i[0]) \
                    .sortBy(lambda x: str(x[1][-4:]) + str(x[1][0:2]) + str(x[1][3:5])) \
                    .map(lambda x: (x[0], x[1], x[2], (int(x[4]) + int(x[5])))) \
                    .map(mapPlazas) \
                    .coalesce(1) \
                    .saveAsTextFile(weekday[1] + "sorted/" + i[1] + i[2])

#filter - filter out the right day of the week
#filter - filter out PM
#filter - filter by Inbound vs Outbound
#sort - sort by date (for easy viewing)
#map - remove the I/O column, add up the E-ZPass and Toll column to get the total number of cars
#map - reassign plaza numbers for convenience
        
# Two folders should be created, InboundPM and OutboundPM
# each containing a file with four columns:
# date, hour, plaza ID number, and number of cars (sum of EZ-Pass and toll)

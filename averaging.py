#! /usr/bin/env python3

import pyspark
import os

def getFields(x):
    fields = x.split("\t")
    date = fields[0]
    try: hour = int(fields[1])
    except: hour = 0
    try: cars = int(fields[2])
    except: cars = 0
    return (date, hour, cars)

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

#For Fridays, for Tuesdays, and for outer boroughs only on Fridays 
for weekday in ["", "T", "M"]:
#for all toll plazas, inbound and outbound
    for plaza in os.listdir(weekday + "sorted2"):
        for direction in os.listdir(weekday + "sorted2/" + plaza):
            #for PM times only (heading home from work)
            if("PM" in direction):
                filename = weekday + "sorted2/" + plaza + "/" +  direction + "/part-00000"
                textFile = sc.textFile(filename)
                a = textFile.map(getFields) \
                            .filter(lambda x: (x[1] == 15 or x[1] == 16 or x[1] == 17) and x[2]!=0) \
                            .map(lambda x: (x[0], (x[2], x[2]*x[1]))) \
                            .reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])) \
                            .map(lambda x: (x[0], (x[1][1] / x[1][0]))) \
                            .map(lambda x: x[0] + "\t" + str(x[1])) \
                            .coalesce(1) \
                            .saveAsTextFile(weekday + 'averaged/'+ plaza + direction)

#filter - 3, 4, and 5 pm only - these are the times that generally have the most cars (see RHfrequencies and TRHfrequencies)
#map (date, (cars on that date at that hour, # of cars*hour))
#reduce (date, (total cars 3-5 PM on that date, total cars 3-5 PM weighted))
#map (date, (weighted total cars / total cars))
#map date \t weighted time when there are most cars

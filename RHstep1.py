#! /usr/bin/env python3

import pyspark
import os

def getFields(x):
    fields = x.split("\t")
    date = fields[0]
    hour = fields[1]
    cars = int(fields[2])
    return (date, (hour, cars))
        
sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

#calculate rush hour as the PM hour with the greatest number of cars, for each
#bridge and tunnel, in each direction, for Fridays and Tuesdays. 
for weekday in ["", "T"]:
    for plaza in os.listdir(weekday + "sorted2"):
        for direction in os.listdir(weekday + "sorted2/" + plaza):
            pathname = weekday + "sorted2/" + plaza + "/" + direction + "/part-00000"
            textFile = sc.textFile(pathname)
            a = textFile.map(getFields) \
                        .reduceByKey(lambda x,y: x if x[1]>y[1] else y) \
                        .map(lambda x: x[0] + "\t" + str(x[1][0])) \
                        .sortBy(lambda x: str(x[6:11]) + str(x[0:2]) + str(x[3:5])) \
                        .coalesce(1) \
                        .saveAsTextFile(weekday + "sorted3/" + plaza + "/" + direction)

#reduceByKey - calculate hour with maximum traffic for each date
#map - date     rushhour
#sortBy - sort by date

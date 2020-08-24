#! /usr/bin/env python3

import pyspark
import os
import glob

def getFields(x):
    fields = x.split("\t")
    plaza = fields[0]
    date = fields[1]
    hour = fields[2]
    cars = fields[3]
    return (plaza, date, hour, cars)

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

#sort the data into a separate folder for each toll plaza
for weekday in ["", "T"]:
    for folder in os.listdir(weekday + "sorted"):
        pathname = weekday + "sorted/" + folder + "/part*"
        for filename in glob.glob(pathname, recursive=True):
            textFile = sc.textFile(filename)
            #for each plaza
            for i in range(1,11):
                saveTo = weekday + "sorted2/plaza" + str(i) + "/" + folder
                a = textFile.map(getFields) \
                            .filter(lambda x: int(x[0]) == i) \
                            .map(lambda x: x[1] + "\t" + x[2] + "\t" + x[3]) \
                            .coalesce(1) \
                            .saveAsTextFile(saveTo)

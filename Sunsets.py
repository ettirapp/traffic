#! /usr/bin/env python3

import pyspark
from datetime import datetime

def getFields(x):
    fields = x.split("\t")
    date = fields[0]
    time = fields[1]
    return (date, time)

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

textFile = sc.textFile('sunsets.txt')

#Filter out sunsets for one weekday only
#Format dates as zero-filled
for weekday in [[1, "tuesday"], [4, "friday"]]:
    a = textFile.map(getFields) \
                .filter(lambda x: datetime.strptime(x[0], "%m/%d/%Y").weekday()==weekday[0]) \
                .map(lambda x: datetime.strptime(x[0], "%m/%d/%Y").strftime("%m/%d/%Y") + "\t" + x[1]) \
                .coalesce(1) \
                .saveAsTextFile(weekday[1] + "Sunsets")

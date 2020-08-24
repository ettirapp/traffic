#! /usr/bin/env python3

import pyspark

def getFields(x):
    fields = x.split("\t")
    plaza = fields[0]
    date = fields[1]
    hour = fields[2]
    cars = fields[3]
    return (plaza, date, hour, cars)

#sort out data for outer boroughs (not Manhattan) only
#(It is unlikely that Sabbath observers who live in Manhattan would be heading
#home to Manhattan on Friday afternoons, because most people who live in Manhattan
#work there as well, so the correlation between sunset and Friday traffic will
#probably be greater when excluding Manhattan-bound traffic.)

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

textFile = sc.textFile("sorted/OutboundPM/part-00000")
#for all plazas (no Outbound traffic has Manhattan as its destination)
for i in range(1,11):
    saveTo = "Msorted2/plaza" + str(i) + "/OutboundPM"
    a = textFile.map(getFields) \
                .filter(lambda x: int(x[0]) == i) \
                .map(lambda x: x[1] + "\t" + x[2] + "\t" + x[3]) \
                .coalesce(1) \
                .saveAsTextFile(saveTo)
    
textFile = sc.textFile("sorted/InboundPM/part-00000")

#for Inbound plazas with a destination that is not Manhattan
for i in [1, 3, 5, 6, 9, 10]:
    saveTo = "Msorted2/plaza" + str(i) + "/InboundPM"
    a = textFile.map(getFields) \
                .filter(lambda x: int(x[0]) == i) \
                .map(lambda x: x[1] + "\t" + x[2] + "\t" + x[3]) \
                .coalesce(1) \
                .saveAsTextFile(saveTo)

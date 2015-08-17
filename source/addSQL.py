#!/usr/bin/env python

import os
import sys
import time
import random


databaseName = 'developmentSimulatorLog'
resultTable = 'demo_application_simulatortestresult'
itemTable = 'demo_application_simulatortestitem'

#please remember to sleep 1


testTypeDict = {}
testTypeDict = {0: 'L3', 1: 'MCU', 2: 'LSU'}


#testConfiguration = 'cpu=POWER%s,mem=%sG,L3=%sM' % (random.randint(4,8), random.randint(12,100), random.randint(2, 30))
#testSoftware = 'Software %s' % random.randint(1, 20)
#testItemIPC = random.random() + 1
#testItemMemoryBandwidth = random.random() + random.randint(800,1000)
#testItemL1MissRate = random.random() + random.randint(8, 15)
#testItemReversedOne = random.randint(1, 20)
#testItemReversedTwo = random.randint(1, 20)
#testItemReversedThree = random.randint(1, 20)

try:
    start = int(sys.argv[1])
    recordLength = int(sys.argv[2])
    stop = start + recordLength
except:
    print 'Usage: %s startID recordLength'
    print 'startID: it means that the id number your will start to insert record into %s and %s' % (resultTable, itemTable)
    print 'recordLength: it means that how many record will you insert into %s and %s' % (resultTable, itemTable)
    sys.exit(0)



for id in range(start, stop):
    resultID = id
    number = random.randint(1429000000, 1439226000)
    string1 = "mysql -uroot -p123456 developmentSimulatorLog " + "-e \"INSERT INTO demo_application_simulatortestresult "
    string2 = "VALUE(%s, 'liangmingquan', 'This is my test comment %s', FROM_UNIXTIME(%s), 'http://10.100.8.185:8090/index.action')\"" % (resultID, resultID, number)
    resultCommand = string1 + string2
    print resultCommand
    os.system(resultCommand)
    ########################################################
    resultID = id
    index = id % 3
    testType = testTypeDict[index]
    testConfiguration = 'cpu=POWER%s,mem=%sG,L3=%sM' % (random.randint(4,8), random.randint(12,100), random.randint(2, 30))
    testSoftware = 'Software %s' % random.randint(1, 20)
    testItemIPC = random.random() + 1
    testItemMemoryBandwidth = random.random() + random.randint(800,1000)
    testItemL1MissRate = random.random() + random.randint(8, 15)
    testItemReversedOne = random.randint(1, 20)
    testItemReversedTwo = random.randint(1, 20)
    testItemReversedThree = random.randint(1, 20)
    string3 = "mysql -uroot -p123456 developmentSimulatorLog " + "-e \"INSERT INTO demo_application_simulatortestitem "
    string4 = "VALUE(%s, %s, FROM_UNIXTIME(%s), '%s', '%s', '%s', %s, %s, %s, %s, %s, %s)\"" % (resultID, resultID, number, testType, testConfiguration, testSoftware, testItemIPC, testItemMemoryBandwidth, testItemL1MissRate, testItemReversedOne, testItemReversedTwo, testItemReversedThree)
    itemCommand = string3 + string4
    print itemCommand
    os.system(itemCommand)
    time.sleep(1)

import os
import time
from django.db import models

# Create your models here.

FLOATDEFAULT = -9.99

class SimulatorTestResult(models.Model):
    testUser = models.CharField('Test User', max_length=30)
    testComment = models.CharField('Test Comment', max_length=100)
    # when I make auto_now_add and auto_now == True, I can not add testRecordTime into fields in SimulatorTestResultAdmin
    #testRecordTime = models.DateTimeField('Record Test Result Time', auto_now=True, auto_now_add=True)
    testRecordTime = models.DateTimeField('Record Test Result Time')
    # add a new field in mysql by SQL, such as: ALTER TABLE demo_application_simulatortestresult ADD COLUMN testResultDetailLink VARCHAR(300) NOT NULL AFTER testRecordTime;
    testResultDetailLink = models.URLField('Test Result URL', verify_exists=False, max_length=300)

    def __unicode__(self):
        return 'User:%s | Record Time:%s' % (self.testUser, self.testRecordTime)

class SimulatorTestItem(models.Model):
    testResult = models.ForeignKey(SimulatorTestResult)
    testTime = models.DateTimeField('When Did The Test')
    testType = models.CharField('Test Type(eg: L3, MCU, LSU etc.)', max_length=20) # eg: L3, MCU, LSU etc.
    testConfiguration = models.CharField('Test Configuration', max_length=50)
    testSoftware = models.CharField('Tool for Test(eg: SpecCPU, Oprofile etc.)', max_length=20)

    testItemIPC = models.FloatField('IPC Value', default = FLOATDEFAULT)
    testItemMemoryBandwidth = models.FloatField('Memory Bandwidth Value(MB/s)', default = FLOATDEFAULT)
    testItemL1MissRate = models.FloatField('L1 Miss Rate(%)', default = FLOATDEFAULT)
    #testItemReversedOne = models.CharField('1st Reversed Item', max_length=20, blank=True)
    #testItemReversedTwo = models.CharField('2nd Reversed Item', max_length=20, blank=True)
    #testItemReversedThree = models.CharField('3th Reversed Item', max_length = 20, blank=True)
    testItemReversedOne = models.FloatField('1st Reversed Item', default = FLOATDEFAULT)
    testItemReversedTwo = models.FloatField('2nd Reversed Item', default = FLOATDEFAULT)
    testItemReversedThree = models.FloatField('3th Reversed Item', default = FLOATDEFAULT)

    def __unicode__(self):
        return 'Test Type:%s | Test Tool: %s | Test Result:%s' % (self.testType, self.testSoftware, self.testTime)


class UploadFilename(models.Model):
    testUser = models.CharField('Test User', max_length=30)
    testComment = models.CharField('Test Comment', max_length=100)
    testRecordTime = models.DateTimeField('Record Test Result Time')
    filename = models.FileField(upload_to = '%Y-%m-%d/%H-%M-%S')
    testResultDetailLink = models.URLField('Test Result URL', verify_exists=False, max_length=300)

    def __unicode__(self):
        return 'Test User:%s | filename: %s | Record Time:%s ' % (self.testUser, os.path.basename(str(self.filename)), self.testRecordTime)


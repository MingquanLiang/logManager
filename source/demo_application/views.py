import os
import re
import time
import datetime
from copy import deepcopy

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper

# add the table(class) defined by user from here
from demo_application.models import SimulatorTestResult as SR
from demo_application.models import SimulatorTestItem as SI
from demo_application.models import UploadFilename as UF
from demo_application.models import FLOATDEFAULT
from demo_application.helper import getAllFieldsMap, reverseGetAllFieldsMap

from ArchApps.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT, DataDebug

# global variable
CODEDEBUG = True
CODEDEBUG = False


def Color_Print(color,*params):
    pList = []
    for param in params:
        pList.append(str(param)) ### turn tuple(params) into list(pList) ###
    colorDict = { 'red':'\033[01;31m', 'green':'\033[01;32m', 'yellow':'\033[01;33m', 'blue':'\033[01;34m', 'magenta':'\033[01;35m', 'cyan':'\033[01;36m', 'white':'\033[01;37m' }
    try:
        if color in colorDict:
            print colorDict[color],' '.join(params),"\033[0m"
    except:
        print str(color)+' '.join(params)

################################### for upload file ############################################
class uploadFileForm(forms.Form):
    """ This form's layout is the same as demo_application.models.UploadFilename. 
    This form is used to control the demo_application.models.UploadFilename indirectly
    """

    testUser = forms.CharField(max_length=20, label='Test User')
    testComment = forms.CharField(max_length=100, label='Test Comment')
    testRecordTime = forms.DateTimeField(label='Test Record Time')
    filename = forms.FileField(label='File Name')
    testResultDetailLink = forms.CharField(max_length=300, label='Test Result URL')

def extractInformationFromAttachment(attachment):
    """ This is a function to parse the attachment uploaded by user.
    It will get useful information include testConfiguration, testSoftware, testType, testTime and all test Items Value.
    """

    attachmentDictNotItem = {}
    attachmentDictItem = {}
    if DataDebug:
        import random
        attachmentDictNotItem['testTime'] = ['When Did The Test', datetime.datetime.now()]
        curSecond = datetime.datetime.now().second
        memory = curSecond + random.randint(1, 10)
        harddisk = curSecond + random.randint(512, 1024)
        if 0 < curSecond < 20:
            attachmentDictNotItem['testType'] = ['Test Type', 'L3']
        elif 20 < curSecond < 40:
            attachmentDictNotItem['testType'] = ['Test Type', 'MCU']
        else:
            attachmentDictNotItem['testType'] = ['Test Type', 'LSU']
        attachmentDictNotItem['testConfiguration'] = ['Test Configuration', 'CPU=POWER8 mem=%sG harddisk=%sG' % (memory, harddisk)]
        attachmentDictNotItem['testSoftware'] = ['Tool for Test', 'Software %s' % curSecond]
        
        #XXX: add the test items dynamically 
        allTestItems = getAllFieldsMap(SI, getAll=False)
        for singleTestItem, verboseName in allTestItems.iteritems():
            attachmentDictItem[singleTestItem] = [verboseName, random.random() + random.randint(10, 20)]
    else:
        attachmentDictNotItem['testTime'] = ['When Did The Test', datetime.datetime.now()]
        attachmentDictNotItem['testType'] = ['Test Type', 'L3']
        #TODO: be careful the 'CRLF'
        with attachment:
            for line in attachment.read().split('\n'):
                lineList = line.split(':')
                lineValue = lineList[1].strip()
                if 'configuration' in lineList[0]:
                    attachmentDictNotItem['testConfiguration'] = ['Test Configuration', lineValue]
                elif 'software' in lineList[0]:
                    attachmentDictNotItem['testSoftware'] = ['Tool for Test', lineValue]
                elif 'IPC' in lineList[0]:
                    attachmentDictItem['testItemIPC'] = ['IPC Value', lineValue]
                elif 'MemoryBandwidth' in lineList[0]:
                    attachmentDictItem['testItemMemoryBandwidth'] = ['Memory Bandwidth', lineValue]
                elif 'L1MissRate' in lineList[0]:
                    attachmentDictItem['testItemL1MissRate'] = ['L1 Miss Rate', lineValue]
                attachmentDictItem['testItemReversedOne'] = ['1st Reversed Item', random.randint(1,20)]
                attachmentDictItem['testItemReversedTwo'] = ['2nd Reversed Item', random.randint(5,25)]
                attachmentDictItem['testItemReversedThree'] = ['3rd Reversed Item', random.randint(10,30)]
                #TODO: ensure the table fields before coding here
                #TODO: I should create a test file to ensure it will be right XXX XXX XXX XXX
                pass
    if CODEDEBUG:
        pass
    return (attachmentDictNotItem, attachmentDictItem)

def uploadFilename(request):
    """ Two mode for user's submission: "Preview Before Submit" and "Sumbit Directly"
    "Preview Before Sumbit": parse the attachment and return a review, user can modify some fields before last submission;
    "Sumbit Directly": parse the attachment and insert all useful into databases.
    """

    if request.method == "POST":
        uploadFileFormObject = uploadFileForm(request.POST, request.FILES)
        #XXX: "Option" is defined in "upload_index.html" 
        uploadOption = request.POST['Option']
        if uploadFileFormObject.is_valid():
            testUser = uploadFileFormObject.cleaned_data['testUser']
            testComment = uploadFileFormObject.cleaned_data['testComment']
            testRecordTime = uploadFileFormObject.cleaned_data['testRecordTime']
            fileName = uploadFileFormObject.cleaned_data['filename']
            testResultDetailLink = uploadFileFormObject.cleaned_data['testResultDetailLink']

            #XXX: DO NOT use absolute path to open the file because the file will not save into filesystem before UF.save() 
            attachmentDictNotItem, attachmentDictItem = extractInformationFromAttachment(fileName) 

            if 'Preview' in uploadOption:
                Color_Print('green', 'Preview Buttom')
                #global echoParseParameter
                echoParseParameter = {}
                editableParameter = {}
                uneditableParameter = {}
                editableParameterNotItem = deepcopy(attachmentDictNotItem)
                editableParameterItem = deepcopy(attachmentDictItem)

                formatTime = editableParameterNotItem['testTime'][1].strftime('%Y-%m-%d %H:%M:%S')
                editableParameterNotItem['testTime'] = ['When Did The Test', formatTime]

                uneditableParameter['testUser'] = testUser
                uneditableParameter['testComment'] = testComment
                uneditableParameter['testRecordTime'] = testRecordTime.strftime('%Y-%m-%d %H:%M:%S')
                uneditableParameter['fileName'] = os.path.basename(fileName.name)
                uneditableParameter['testResultDetailLink'] = testResultDetailLink

                echoParseParameter['STATIC_URL'] = STATIC_URL
                echoParseParameter['uneditableParameter'] = uneditableParameter
                echoParseParameter['editableParameterNotItem'] = editableParameterNotItem
                echoParseParameter['editableParameterItem'] = editableParameterItem
                return render_to_response('demo_application/upload/upload_echo.html', echoParseParameter)
            else: # Sumbit Directly ===> it is OK if ensure the table fields name
                Color_Print('green', 'Sumbit Directly')
                # update the data into UF()    
                ufObject = UF()
                ufObject.testUser = testUser
                ufObject.testComment = testComment
                ufObject.testRecordTime = testRecordTime
                ufObject.filename = fileName
                ufObject.testResultDetailLink = testResultDetailLink
                ufObject.save()

                # upload the data into SR()
                srObject = SR()
                srObject.testUser, srObject.testComment, srObject.testRecordTime, srObject.testResultDetailLink = testUser, testComment, testRecordTime, testResultDetailLink
                srObject.save()
                foreignKeyID = srObject.id

                # upload the data into SI()
                siObject = SI()
                siObject.testResult_id, siObject.testTime, siObject.testType, siObject.testConfiguration, siObject.testSoftware = foreignKeyID, attachmentDictNotItem['testTime'][1], attachmentDictNotItem['testType'][1], attachmentDictNotItem['testConfiguration'][1], attachmentDictNotItem['testSoftware'][1]
                # TODO: this is the test Items, it can NOT code before ensuring the table fields

                for singleTestItem in getAllFieldsMap(SI, getAll=False):
                    siObject.__setattr__(singleTestItem, attachmentDictItem[singleTestItem][1])
                siObject.save()
                return HttpResponseRedirect(reverse('demo_application.views.postUploadFilename'))
    else:
        uploadFileFormObject = uploadFileForm()
    return render_to_response('demo_application/upload/upload_index.html', {'uploadFileFormObject': uploadFileFormObject, 'STATIC_URL':STATIC_URL})

def echoUploadFilename(request):
    """ This funtion is to preview the attachment parsed for user, and user can modify some fields before last submission.
    In here, get the parameters from "uploadFilename" via global variable, I think it is NOT the best choice.
    """
    if request.method == 'POST':
        postDict = request.POST
        Color_Print('magenta', '[%s]' % request.POST)
        # uneditable fields
        testUser = postDict.get('testUser')
        testComment = postDict.get('testComment')
        testRecordTime = datetime.datetime.strptime(postDict.get('testRecordTime'), '%Y-%m-%d %H:%M:%S')
        fileName = postDict.get('fileName')
        testResultDetailLink = postDict.get('testResultDetailLink')

        # editable fields
        testTime = datetime.datetime.strptime(postDict.get('testTime'), '%Y-%m-%d %H:%M:%S')
        testType = postDict.get('testType')
        testConfiguration = postDict.get('testConfiguration')
        testSoftware = postDict.get('testSoftware')

        # These test Items is dynamically added as below

        # update the data into UF()
        curTime = time.strftime('%Y-%m-%d/%H-%M-%S')
        ufObject = UF()
        ufObject.testUser = testUser
        ufObject.testComment = testComment
        ufObject.testRecordTime = testRecordTime
        ufObject.filename = curTime + '/'+ fileName
        ufObject.testResultDetailLink = testResultDetailLink
        ufObject.save()

        # upload the data into SR()
        srObject = SR()
        srObject.testUser, srObject.testComment, srObject.testRecordTime, srObject.testResultDetailLink = testUser, testComment, testRecordTime, testResultDetailLink
        srObject.save()
        foreignKeyID = srObject.id

        # upload the data into SI()
        siObject = SI()
        siObject.testResult_id, siObject.testTime, siObject.testType, siObject.testConfiguration, siObject.testSoftware = foreignKeyID, testTime, testType, testConfiguration, testSoftware 
        # TODO: this is the test Items, it can NOT code before ensuring the table fields
        for singleTestItem in getAllFieldsMap(SI, getAll = False):
            try:
                siObject.__setattr__(singleTestItem, float(postDict.get(singleTestItem)))
            except:
                siObject.__setattr__(singleTestItem, -9.99)
        siObject.save()
        return HttpResponseRedirect(reverse('demo_application.views.postUploadFilename'))


def postUploadFilename(request):
    parseParameter = {}
    parseParameter['STATIC_URL'] = STATIC_URL
    return render_to_response('demo_application/upload/upload_post.html', parseParameter)

################################### for download file ############################################

def getDownloadFileInformation():
    """ Get all information of "UploadFilename" from database """

    downloadFileList = []
    allDownloadFileObjects = UF.objects.all()
    for downloadFileObject in allDownloadFileObjects:
        # some attributes defined when upload
        testUser = downloadFileObject.testUser
        testComment = downloadFileObject.testComment
        testRecordTime = downloadFileObject.testRecordTime.strftime('%Y-%m-%d %H:%M:%S')
        downloadFile = downloadFileObject.filename
        #download file url should be: http://IP:port/downloading/downloadFile

        fileName = os.path.basename(downloadFile.name)
        uploadDateTime = os.path.dirname(downloadFile.name).split('/')
        uploadDate = uploadDateTime[0]
        uploadTime = uploadDateTime[1].replace('-', ':')

        downloadFileMap = {}
        downloadFileMap = {'downloadFile': downloadFile, 'testUser': testUser, 'testComment': testComment, 'testRecordTime': testRecordTime, 'fileName': fileName, 'uploadDate': uploadDate, 'uploadTime': uploadTime}
        downloadFileList.append(downloadFileMap)
    return downloadFileList

def downloadFilename(request):
    """ render the download list to web page """

    parseParameter = {}
    downloadFileList = getDownloadFileInformation()
    parseParameter['downloadFileList'] = downloadFileList
    parseParameter['STATIC_URL'] = STATIC_URL
    parseParameter['MEDIA_URL'] = MEDIA_URL
    return render_to_response('demo_application/download/download_index.html', parseParameter)

################################## for search file #######################################################
def searchIndex(request):
    allAttribute = getAllFieldsMap(SI, getAll=False)
    testItemList = []
    for fieldName, fieldAliasName in allAttribute.iteritems():
        testItemList.append(fieldAliasName)
    testTypeList = list(set([i.testType for i in SI.objects.all()]))
    parseParameter = {}
    parseParameter['testItemList'] = sorted(testItemList)
    parseParameter['testTypeList'] = sorted(testTypeList)
    parseParameter['STATIC_URL'] = STATIC_URL
    return render_to_response('demo_application/search/search_index.html', parseParameter)

def searchResult(request):
    displayForm = str(request.POST.get('Display As')).strip()
    testType = request.POST.get('Test Type')
    testItem = request.POST.get('Key Word')
    startTime = request.POST.get('Start Time')
    endTime = request.POST.get('End Time')
    if CODEDEBUG == True:
        Color_Print('green', 'startTime=[%s] and endTime=[%s]' % (startTime, endTime))
    userParameter = {}
    userParameter['testType'] = testType
    userParameter['testItem'] = testItem
    userParameter['startTime'] = startTime
    userParameter['endTime'] = endTime
    if displayForm == 'table':
        #return HttpResponseRedirect(reverse('demo_application.views.tableResult'))
        return tableResult(userParameter)
    elif displayForm == 'figure':
        #return HttpResponseRedirect(reverse('demo_application.views.figureResult'))
        return figureResult(userParameter)
    else:
        return HttpResponse('Failed to Get any information. Please choose correct display form')

def filterDataFromDatabase(testType, startTime, endTime):
    if CODEDEBUG == True:
        xx = SI.objects.filter(testType__exact=testType).order_by('testTime')
        for a in xx:
            Color_Print('yellow', '%s and value=[%s]' % (a, a.testItemIPC))
    """
    get selected data from database, equal to SQL: 
    select testUser, testComment, testRecordTime, testTime, testType, testConfiguration, testSoftware, testItemIPC \
    FROM demo_application_simulatortestresult INNER JOIN demo_application_simulatortestitem \
    WHERE demo_application_simulatortestresult.id = demo_application_simulatortestitem.testResult_id and testType="L3" ORDER BY testTime;
    """
    if startTime == "" and endTime == "":
        allSIObject = SI.objects.filter(testType__exact=testType).order_by('testTime') 
    else:
        try:
            startTimeFormat = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
            endTimeFormat = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            Color_Print('red', 'One of Start Time and End Time may be empty. Dump the time: Start Time=[%s] and End Time=[%s]' % (startTime, endTime))
            allSIObject = SI.objects.filter(testType__exact=testType).order_by('testTime')
        else:
            ### when endTime < startTime, it will return empty ###
            allSIObject = SI.objects.filter(testType__exact=testType).order_by('testTime').filter(testTime__gte=startTimeFormat).filter(testTime__lte=endTimeFormat)
    return allSIObject

def tableResult(userParameter):
    """ This function: 1) Get user's online submission ; 2) Get and filter data from database 3) display as table """

    testType = userParameter['testType']
    testItem = userParameter['testItem']
    startTime = userParameter['startTime']
    endTime = userParameter['endTime']


    allSIObject = filterDataFromDatabase(testType, startTime, endTime)
    assert allSIObject != None, 'Failed To filter data, Please check user submission: testType=[%s], testItem=[%s], startTime=[%s], endTime=[%s]' % (testType, testItem, startTime, endTime)

    if len(allSIObject) == 0:
        parseParameter = {}
        parseParameter['testType'] = testType
        parseParameter['testItem'] = testItem
        parseParameter['no_data'] = 'no_data'
        parseParameter['STATIC_URL'] = STATIC_URL
        return render_to_response('demo_application/search/table_result.html', parseParameter)

    testResult = {}
    allItems = reverseGetAllFieldsMap(getAllFieldsMap(SI, getAll=False))
    for i in allSIObject:
        testItemName = allItems[testItem]
        #testResult[(i.testSoftware, i.testConfiguration)] = getattr(i, testItemName) # show horizontally
        testResult[(i.testConfiguration, i.testSoftware)] = getattr(i, testItemName)  # show vertically
    testRow = list(set([i[0] for i in testResult]))
    testColumn = list(set([i[1] for i in testResult]))
    testValue = []
    for everyRow in testRow:
        #testValue.append([testResult.get((everyRow, everyColumn), '-') for everyColumn in testColumn])
        tempList = []
        for everyColumn in testColumn:
            value = testResult.get((everyRow, everyColumn), '-')
            if value == FLOATDEFAULT:
                value = '-'
            tempList.append(value)
        testValue.append(tempList)

    columnLength = len(testColumn)
    if CODEDEBUG == True:
        Color_Print('green', 'Row is [%s] and Column is [%s] and Value is [%s]' % (testRow, testColumn, testValue))
        Color_Print('green', 'Value is [%s]' % testValue)

    assert len(testRow) == len(testValue), 'testRow is [%s] and testValue is [%s]' % (testRow, testValue)
    #if len(testRow) != len(testValue):
    #    return render_to_response('demo_application/search/search_error.html', {})

    testRowAndValueList = []
    for index in range(len(testRow)):
        testRowAndValueList += [testRow[index]] + testValue[index]
    testRowIndexList = [index for index in range(len(testRowAndValueList)) if testRowAndValueList[index] in testRow ]
    testValueIndexList = []
    for i in testRowIndexList:
        testValueIndexList.append(int(i) + len(testValue[0]))

    parseParameter = {}
    parseParameter['testResult'] = testResult
    parseParameter['testType'] = testType
    parseParameter['testItem'] = testItem
    parseParameter['testColumn'] = testColumn
    parseParameter['columnLength'] = columnLength
    parseParameter['testRowAndValueList'] = testRowAndValueList
    parseParameter['testRowIndexList'] = testRowIndexList
    parseParameter['testValueIndexList'] = testValueIndexList
    parseParameter['STATIC_URL'] = STATIC_URL

    return render_to_response('demo_application/search/table_result.html', parseParameter)

def figureResult(userParameter):
    """ This function: 1) Get user's online submission ; 2) Get and filter data from database 3) display as figure """


    testType = userParameter['testType']
    testItem = userParameter['testItem']
    startTime = userParameter['startTime']
    endTime = userParameter['endTime']


    allSIObject = filterDataFromDatabase(testType, startTime, endTime)
    assert allSIObject != None, 'Failed To filter data, Please check user submission: testType=[%s], testItem=[%s], startTime=[%s], endTime=[%s]' % (testType, testItem, startTime, endTime)

    allSIObjectList = []
    allItems = reverseGetAllFieldsMap(getAllFieldsMap(SI, getAll=False))
    for siObject in allSIObject:
        siObjectMap = {}
        testItemName = allItems[testItem]
        ### *** field from SI(id is primary key and testResult_id is foreign key, and can refer to SR via testResult) ***
        id = siObject.id
        #testResult_id = siObject.testResult_id
        testResult = siObject.testResult
        value = getattr(siObject, testItemName)
        if value == FLOATDEFAULT:
            continue
        testSoftware = siObject.testSoftware
        testConfiguration = siObject.testConfiguration

        ### it is a <type 'datetime.datetime'> object
        testTime = siObject.testTime
        year = testTime.year
        ### *** attention, when pass into Html, month should be minus 1 ***
        month = int(testTime.month) - 1 
        day = testTime.day
        hour = testTime.hour
        minute = testTime.minute
        second = testTime.second

        ### *** field from SR by foreign key: testResult_id is the foreign key of SI reference on SR(its primary key is id) ***
        testUser = testResult.testUser
        testComment = testResult.testComment
        #testRecordTime = testResult.testRecordTime
        testResultDetailLink = testResult.testResultDetailLink

        siObjectMap = { 'id': id, 'value': value, 'testSoftware': testSoftware, 'testConfiguration': testConfiguration, \
                        'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute, 'second': second, \
                        'testUser': testUser, 'testComment': testComment, 'testResultDetailLink':testResultDetailLink }
        allSIObjectList.append(siObjectMap)
    testResultLength = len(allSIObjectList)

    parseParameter = {}
    parseParameter['testType'] = testType
    parseParameter['testItem'] = testItem
    parseParameter['allSIObjectList'] = allSIObjectList
    parseParameter['testResultLength'] = testResultLength
    parseParameter['STATIC_URL'] = STATIC_URL

    return render_to_response('demo_application/search/figure_result.html', parseParameter)



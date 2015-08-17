def getAllFieldsMap(modelName, getAll=True):
    allFieldNames = modelName._meta.get_all_field_names()
    allFields = modelName._meta.fields
    allFieldsMap = {}
    for field in allFields:
        fieldVerboseName = field.verbose_name
        fieldName = field.name
        if getAll == False: 
            if 'testItem' in fieldName:
                allFieldsMap[fieldName] = fieldVerboseName
        else:
            allFieldsMap[fieldName] = fieldVerboseName
    # key is fieldName(defined in database) and value is its alias name
    return allFieldsMap

def reverseGetAllFieldsMap(allFieldsMap):
    """ exchange the key and value of dict """

    newAllFieldsMap = {}
    for key, value in allFieldsMap.iteritems():
        newAllFieldsMap[value] = key
    return newAllFieldsMap

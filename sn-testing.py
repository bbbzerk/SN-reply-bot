import requests

# Specify SN instance
instance = 'dev68539'

# Set the request parameters
url = 'https://' + instance + '.service-now.com/api/now/table/'
user = 'python_svc'
pwd = 'B$7Ge9gn!J9mU#R1IgyGXNCqx%7L5l$5'
# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

'''Gets a record from ServiceNow
@parms: table  - Table of the record to get.
        number - number of the record.
@returns: json encoded response with the record data.
'''
def getRecord(table, number):
    myTable = str(table)
    myNumber = str(number)
    return requests.get(url + myTable + '?sysparm_query=number%3D' + myNumber, auth=(user, pwd), headers=headers).json()


'''Puts relevant data into and returns a JSON object.

@params: jsonData - JSON encoded data object with all raw data fron ServiceNow.

@returns: JSON object containing relevant information about the record.
          If there is no result from SN the return value has an 'error' key of True.
          If there IS a good result the 'error' key has a value of False.
'''
def formatReturn(jsonData):
    
    # Need to make sure it's a good result from SN
    if len(jsonData['result']) > 0:
        myData = jsonData['result'][0]
        number = myData['number']
        shortDesc = myData['short_description']
        sysClass = myData['sys_class_name']
        sysId = myData['sys_id']
        theUser = ''
        
        # Get user's name (caller, requested for)
        if sysClass == 'incident':
            caller_id_link = myData['caller_id']['link']
            theCallerRaw = requests.get(caller_id_link, auth=(user,pwd), headers=headers)
            if theCallerRaw.status_code != 200:
                theUser = ''
            else:
                theCallerData = theCallerRaw.json()
                theUser = theCallerData['result']['name']
        elif sysClass == 'sc_task':
            request_link = myData['request']['link']
            requestRaw = requests.get(request_link, auth=(user,pwd), headers=headers)
            if requestRaw.status_code != 200:
                theUser = ''
            else:
                requestData = requestRaw.json()
                requested_for_link = requestData['result']['requested_for']['link']
                requested_for_raw = requests.get(requested_for_link, auth=(user,pwd), headers=headers)
                if requested_for_raw.status_code != 200:
                    theUser = ''
                else:
                    requested_for_data = requested_for_raw.json()
                    theUser = requested_for_data['result']['name']
        
        recordLink = "https://" + instance + ".service-now.com/nav_to.do?uri=%2F" + sysClass + ".do%3Fsys_id%3D" + sysId

        # Build JSON to return
        theReturn = {}
        theReturn['error'] = False
        theReturn['button'] = ":ticket: " + str(recordLink)
        theReturn['number'] = number
        theReturn['shortDesc'] = shortDesc
        theReturn['link'] = recordLink
        if (theUser):
            theReturn['user'] = theUser

        return theReturn

    # Otherwise there was not match
    else:
        theReturn = {}
        theReturn['error'] = True

        return theReturn


# Tests
good = getRecord('incident','INC0010002')
print('Good: ' + str(good))
print()
print('Good Result Length: ' + str(len(good['result'])))
print()

bad = getRecord('incident','INC9999999')
print('Bad: ' + str(bad))
print('Bad Result Length: ' + str(len(bad['result'])))

badFormat = formatReturn(bad)
if badFormat['error'] == True:
    print('True')
elif badFormat['error'] == False:
    print('False')

goodFormat = formatReturn(good)
if goodFormat['error'] == True:
    print('True')
elif goodFormat['error'] == False:
    print('False')

print()
print(goodFormat)
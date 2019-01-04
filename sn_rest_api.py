'''Communicates with Service-Now REST API.

Methods:
 - getRecord(table,number) 
 - formatReturn(jsonData)
 - printMyRecord(jsonRecord)
'''
import requests

# Specify SN instance
instance = 'dev68539'

# Set the request parameters
url = 'https://' + instance + '.service-now.com/api/now/table/'
user = 'python_svc'
pwd = 'B$7Ge9gn!J9mU#R1IgyGXNCqx%7L5l$5'
# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}


'''Puts relevant data into and returns a JSON object.

@params: jsonData - JSON encoded data object with all raw data fron ServiceNow.

@returns: JSON object containing relevant information about the record.
'''
def formatReturn(jsonData):

    # Need to make sure it's a good result from SN and return error: False
    if len(jsonData['result']) > 0:
        myData = jsonData['result'][0]
        number = myData['number']
        shortDesc = myData['short_description']
        sysClass = myData['sys_class_name']
        sysId = myData['sys_id']
        theUser = ''
        ticketIcon = ''
        
        # Get user's name (caller or requested for)
        if sysClass == 'incident':
            ticketIcon = ':ticket: '
            caller_id_link = myData['caller_id']['link']
            theCallerRaw = requests.get(caller_id_link, auth=(user,pwd), headers=headers)
            if theCallerRaw.status_code != 200:
                theUser = ''
            else:
                theCallerData = theCallerRaw.json()
                theUser = theCallerData['result']['name']

        elif sysClass == 'sc_task' or sysClass == 'sc_req_item':
            ticketIcon = ':shopping_trolley: '
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

        elif sysClass == 'sc_request':
            ticketIcon = ':shopping_trolley: '
            requested_for_link = myData['requested_for']['link']
            requested_for_raw = requests.get(requested_for_link, auth=(user,pwd), headers=headers)
            if requested_for_raw.status_code != 200:
                theUser = ''
            else:
                requested_for_data = requested_for_raw.json()
                theUser = requested_for_data['result']['name']

        elif sysClass == 'kb_knowledge':
            ticketIcon = ':book: '
        
        if sysClass == 'kb_knowledge':
            recordLink = "https://" + instance + ".service-now.com/kb_view.do?sysparm_article=" + number
        else:
            recordLink = "https://" + instance + ".service-now.com/nav_to.do?uri=%2F" + sysClass + ".do%3Fsys_id%3D" + sysId

        # Build JSON to return
        theReturn = {}
        theReturn['error'] = False
        theReturn['number'] = number
        theReturn['ticketIcon'] = ticketIcon
        if (shortDesc):
            theReturn['shortDesc'] = shortDesc
        else:
            theReturn['shortDesc'] = ''
        theReturn['link'] = recordLink
        if (theUser):
            theReturn['user'] = theUser
        else:
            theReturn['user'] = ''

        return theReturn

    # Otherwise there was no match, return error: True
    else:
        theReturn = {}
        theReturn['error'] = True

        return theReturn


'''Builds a string of the JSON object info that looks nice.

@params: JSON object with record info.

@returns: String containing the relevant information about the record.

'''
def printMyRecord(jsonRecord):
    printStr = ''
    printStr += '*Number:* ' + jsonRecord['number'] + '\n'
    if jsonRecord['shortDesc']:
        printStr += '*Short Description:* ' + jsonRecord['shortDesc'] + '\n'
    if jsonRecord['user']:
        printStr += '*User:* ' + jsonRecord['user'] + '\n'
    return printStr


'''Gets a record from ServiceNow
@parms: table  - Table of the record to get.
        number - number of the record.
@returns: json encoded response with the record data.
'''
def getRecord(table, number):
    myTable = str(table)
    myNumber = str(number)
    return requests.get(url + myTable + '?sysparm_query=number%3D' + myNumber, auth=(user, pwd), headers=headers).json()


# TESTING!!
# Test the method by calling with test data
#response = getRecord('sc_req_item','RITM0010002')
# Decode the JSON response into a dictionary and use the data
#data = response.json()
#print(formatReturn(data))
#print(getRecord('sc_req_item','RITM0010002'))
#print()
#print()
#print(formatReturn(getRecord('sc_req_item','RITM0010002')))
#print(printMyRecord(formatReturn(getRecord('sc_req_item','RITM0010002'))))
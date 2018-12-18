from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import sn_rest_api
import json
import os
import re

# Import environmental variables that contain
# the bot token and signing secret.
token = os.environ.get('BOT_TOKEN')
signing = os.environ.get('APP_SIGNING_SECRET')

slack_events_adapter = SlackEventAdapter(signing, "/slack/events")
slack_client = SlackClient(token)

# Event handling for receiving a message event from Slack.
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    channel = message["channel"]
    text = str(message.get('text'))
    match = matchText(text)
    matchLen = len(match)
    if message.get("subtype") is None and matchLen > 0:
        if matchLen == 1:
                number = str(match[0])
                print('Entered if statement for matchLen == 1')
                snTable = setTable(match[0])
                print()
                print('SN Table: ' + snTable)
                print()
                print('Number: ' + number)
                response = sn_rest_api.formatReturn(sn_rest_api.getRecord(snTable,number))
                print()
                print("Response: ")
                #print(response)
                strText = sn_rest_api.printMyRecord(response)
                print()
                print('Formatted String Text: ' + strText)
                
                button = [
                        {
                                "fallback": "Open record " + str(match[0]),
                                "actions": [
                                        {
                                                "type": "button",
                                                "text": "🎫 " + str(match[0]),
                                                "url": str(response["link"])
                                        }
                                ]
                        }
                ]
                
        
                
                slack_client.api_call("chat.postMessage", channel=channel, text=strText, attachments=button)

        else:
                for index in match:
                        myMessage += str(match[index]) + ' '

                channel = message["channel"]
        #send_message = "Responding to recognized message sent by user <@%s>." % message["user"]
        #send_message += "You said: " + myMessage
        #slack_client.api_call("chat.postMessage", channel=channel, text=send_message)
        


'''Matches the ServiceNow regex patten agains the string paramter

@params: string to match

@returns: Array of matches. If no results returns an array of length 0.
'''
def matchText(str):
        return re.findall(r'INC\d{7}|REQ\d{7}|RITM\d{7}|SCTASK\d{7}|KB\d{7}', str)

'''Takes an input and defines a SN table based on that text.

@params: string to match.

@returns: Table value as a string.
'''
def setTable(str):
        myTable = ''
        if "INC" in str:
                myTable = 'incident'
        elif "REQ" in str:
                myTable = 'sc_request'
        elif "RITM" in str:
                myTable = 'sc_req_item'
        elif "SCTASK" in str:
                myTable = 'sc_task'
        elif "KB" in str:
                myTable = 'kb_knowledge'
        return myTable


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)
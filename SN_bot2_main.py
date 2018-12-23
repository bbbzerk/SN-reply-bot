from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import sn_rest_api, json, os, re

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

        # If message in a thread, reply to that thread
        myThread = ''
        if message.get('thread_ts') is not None:
                myThread = message['thread_ts']

        # subtype none prevents the system from responding to the bot's message events
        if message.get("subtype") is None and matchLen > 0:
                if matchLen == 1:
                        number = str(match[0])
                        snTable = setTable(match[0])
                        response = sn_rest_api.formatReturn(sn_rest_api.getRecord(snTable,number))
                        
                        # If SN returns a good record, print it to Slack
                        if response['error'] == False:
                                strText = sn_rest_api.printMyRecord(response)
                                button = [{
                                                "fallback": "Open record " + str(match[0]),
                                                "actions": [{
                                                                "type": "button",
                                                                "text": "🎫 " + str(match[0]),
                                                                "url": str(response["link"])
                                                        }]
                                        }]       

                                # Make slack api call postMessage with above information     
                                slack_client.api_call("chat.postMessage", channel=channel, text=strText, attachments=button, thread_ts=myThread)
                        
                        #Otherwise if SN returns no record, print to Slack no record found
                        elif response['error'] == True:
                                strText = "No results for record: *" + number + "*."
                                slack_client.api_call("chat.postMessage", channel=channel, text=strText, thread_ts=myThread)


                elif message.get("subtype") is None and matchLen > 1:
                        for textMatch in match:
                                number = str(textMatch)
                                snTable = setTable(textMatch)
                                response = sn_rest_api.formatReturn(sn_rest_api.getRecord(snTable,number))
                                strText = sn_rest_api.printMyRecord(response)
                                button = [{
                                        "fallback": "Open record " + number,
                                        "actions": [{
                                                        "type": "button",
                                                        "text": "🎫 " + number,
                                                        "url": str(response["link"])
                                                }]
                                }]
                                # Make slack api call postMessage with above information for each record in match array
                                slack_client.api_call("chat.postMessage", channel=channel, text=strText, attachments=button, thread_ts=myThread)

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
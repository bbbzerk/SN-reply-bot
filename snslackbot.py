from slackclient import SlackClient
import time
import os

token = os.environ.get('SLACKBOT_SN_TOKEN')

slack_client = SlackClient(token)

link = '<https://imgflip.com/s/meme/That-Would-Be-Great.jpg|That would be great>'

if slack_client.rtm_connect():
    while True:
        events = slack_client.rtm_read()
        for event in events:
            if (
                'channel' in event and
                'text' in event and
                event.get('type') == 'message'
            ):
                channel = event['channel']
                text = event['text']
                if 'test123' in text.lower() and link not in text:
                    slack_client.api_call(
                        'chat.postMessage',
                        channel=channel,
                        text=link,
                        as_user='true:'
                    )
        time.sleep(1)
else:
    print('Connection failed, invalid token?')

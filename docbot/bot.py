import os,string
import time
import datetime
from slack.slack_commands import parse_bot_commands, output_command
from config import slack_client, log_commands_path
from nlp.nlp_commands import handle_command
import pandas as pd
import json


# Initialize with empty value to start the conversation.
context = {}
current_action = ''
follow_ind = 0
session_df = pd.DataFrame({},columns=['timestamp', 'user', 'context']) #stores the session details of the user
# bot's user ID in Slack: value is assigned after the bot starts up
bot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM

if current_action == 'end_conversation': # Based on the this, the context variables are reset
  session_df = session_df[session_df.user != message_user+channel]
  context = {}
  current_action = ''


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Kelly connected and running!")
        
        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]
        
        while True:
            user_id,message_user,message,team,channel,start_timestamp  = parse_bot_commands(slack_client.rtm_read(),bot_id) #slack processing
            
            if message: # If a User has typed something in Slack
                try:
                    context = json.loads(session_df.loc[session_df.user == message_user+channel,'context'].values[0])
                except:
                    context = {}
                    session_df = session_df.append({'timestamp': start_timestamp, 'user': message_user+channel, 'context': json.dumps(context)}, ignore_index=True)
                    
                context,slack_output,current_action = handle_command(message,channel, message_user,context) #nlp processing
                session_df.loc[session_df.user == message_user+channel,'context'] = json.dumps(context)
                output_command(channel, slack_output) #slack processing
                conversation_id = context['conversation_id']
                
                try:
                    if context['currentIntent'] in ['anything_else']:
                        follow_ind = 1
                    else:
                        follow_ind = 0
                except:
                    pass
                
                if current_action == 'end_conversation': # Based on the this, the context variables are reset
                    session_df = session_df[session_df.user != message_user+channel]
                    context = {}
                    current_action = ''
                
                end_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                processing_time = str((datetime.datetime.strptime(end_timestamp, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(start_timestamp, '%Y-%m-%d %H:%M:%S')).total_seconds())
                
                string_to_run = string.Template("""python3 -W ignore "${log_commands_path}" "${user_id}" "${message_user}" "${conversation_id}" "${message}" "${slack_output}" "${team}" "${channel}" "${start_timestamp}" "${end_timestamp}" "${processing_time}" "${follow_ind}" &""").substitute(locals()) #logs processing
                os.system(string_to_run)
                
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")



def parse_bot_commands(slack_events,bot_id):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                message_user = event['user']
                team = event['team']
                channel = event['channel']
                start_timestamp = datetime.datetime.fromtimestamp(float(event['event_ts'])).strftime('%Y-%m-%d %H:%M:%S')
                return user_id,message_user,message,team,channel,start_timestamp
    return None, None, None, None, None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def output_command(channel,slack_output):
    """
        Output bot command via the slack channel
    """
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=slack_output
    )


def file_upload(channel, filename):
    with open(filename,'rb') as file_content:
        slack_client.api_call(
        "files.upload",
        channels=channel,
        file=file_content
        )


def slack_tiles(channel, search_term, title, title_url, image_url):
    attachments_json = [
            {
                "title": title.values[0],
                "title_link": title_url.values[0],
                "image_url": image_url.values[0]
            },
            {
                "title": title.values[1],
                "title_link": title_url.values[1],
                "image_url": image_url.values[1]
            },
            {
                "title": title.values[2],
                "title_link": title_url.values[2],
                "image_url": image_url.values[2]
            }
        ]
  
    # Send a message with the above attachment, asking the user if they want coffee
    slack_client.api_call(
      "chat.postMessage",
      channel=channel,
      text='Recommendations for "' + str(search_term) + '"',
      attachments=attachments_json
    )      


def message_buttons(channel, button, url, search_term):
    attachments_json = [
        {
            "text": " ",
            "fallback": "You didn't make a selection",
            "callback_id": "code_search",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "code_link",
                    "text": "1. " + button.values[0],
                    "type": "button",
                    "url": url.values[0]
                },
                {
                    "name": "code_link",
                    "text": "2. " + button.values[1],
                    "type": "button",
                    "url": url.values[1]
                },
                {
                    "name": "code_link",
                    "text": "3. " + button.values[2],
                    "type": "button",
                    "url": url.values[2]
                },
                {
                    "name": "code_link",
                    "text": "4. " + button.values[3],
                    "type": "button",
                    "url": url.values[3]
                },
                {
                    "name": "code_link",
                    "text": "5. " + button.values[4],
                    "type": "button",
                    "url": url.values[4]
                }
            ]
        }
    ]

    # Send a message with the above attachment, asking the user if they want coffee
    slack_client.api_call(
      "chat.postMessage",
      channel=channel,
      text=search_term,
      attachments=attachments_json
    )

#bot user auth token = xoxb-625889502832-619565425937-m4KbyZbfyBl7cpdR1N0VMYvM
#o auth token = xoxp-625889502832-628047413542-619565421665-4cbb05fddf7d5b4c6b3694b108218c9c

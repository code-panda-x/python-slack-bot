import slack
import random
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

# Oauth token gives bot permission to do stuff in the channel
client = slack.WebClient("your-oath-token")


app = Flask(__name__)
# Basic Information - Signing secret
# When event happens, slack sends http post requests to our webserver: app (thru our ngrok tunnel specified in request URL)
# All the events are sent to this end point: /slack/events, if we change it we need to update it in slack reqeust URL
# Adapter contains all the events info
slack_event_adapter = SlackEventAdapter(
    "your-signing-sercret", '/slack/events', app)

# Get ID of bot
BOT_ID = client.api_call("auth.test")['user_id']
message_counts = {}

# Handle message event


@slack_event_adapter.on('message')
# Payload is data SlackAPI sent to us
def message(payload):
    event = payload.get('event', {})  # if event not found, return null
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    # print(payload)
    if BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1
        if "flip a coin" in text.lower():
            rand = random.randint(0, 1)
            if rand == 0:
                result = "Heads"
            else:
                result = "Tails"
            # Send message back to channel by client
            client.chat_postMessage(channel=channel_id, text=result)
        else:
            client.chat_postMessage(channel=channel_id, text=text)

# Slash commands
# Add new routes to app


@app.route('/message-count', methods=['POST'])
def message_count():
    data = request.form
    # print(data)
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(
        channel=channel_id, text=f"Message: {message_count}")
    return Response(), 200


# run flask app on defalut port
# Debug=True auto update web server
if __name__ == "__main__":
    app.run(debug=True)

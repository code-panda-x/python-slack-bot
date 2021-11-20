# Created a Slack bot in Python

Wrote a simple logic that slack bot will repeat the messages you sent. But if you say "flip a coin", the bot will return "Heads" or "Tails" randomly

## Simple Logic

When event happens, slack sends http post requests to negork webserver (negork reroutes to our local server flask app). Then we handle the requests and send responses back.

## Dependencies
```
pip3 install slackclient

pip3 install flask

pip3 install slackeventsapi

brew install --cask ngrok
```
## Slack API Setup

- Event subscriptions: request URL: "http://your-ngrok-url/slack/events"
- Slash command: "http://your-ngrok-url/nessage-count"

# Run
```
python3 bot.py

./ngrok http 5000
```
## Gotchas

Everytime you close ngork, you should reset your URL in slack API

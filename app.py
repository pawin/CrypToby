from flask import Flask, request, abort, json
import os
import time
from slackclient import SlackClient
import cmc_api as api

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

app = Flask(__name__)

@app.route("/info", methods=['GET'])
def server_info():
    return "woof woof"

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if command.startswith('$'):
        """
            Find data from coin market cap
        """
        symbol = command.replace("$","")

        response = ""
        if symbol == 'mcap':
            response = "```" + api.findGlobalData() + "```"
        else:
            response = "```" + api.findCoinMarketCapPrice(symbol) + "```"

        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:# and AT_BOT in output['text']:
                return output['text'], output['channel']
                # return text after the @ mention, whitespace removed
                # return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Bot is connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

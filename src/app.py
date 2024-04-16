# -*- coding: utf-8 -*-
import os, logging
from dotenv import load_dotenv
import slack_bolt
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient

# LLM functions and objects
from utils.config import MAP_MODEL_ID, MODEL
from utils.llm_model import build_chain, add_chain_link, THREADS_DICT
from utils.regex_funcs import re_get_mentions
# Credentials
load_dotenv()
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)
logger = logging.getLogger(__name__)

# ====================================
# Slack event listeners
# ====================================

@app.message(".*")
def message_handler(message: dict, say: slack_bolt.Say, logger: logging.Logger) -> None:
    """
    Listener for all messages in Apps and Channels
        including messages to chatbot within Apps
    
    Parameters
    ----------
    message : dict
        message received from Slack user in Apps
    
    say : slack_bolt.Say
        sends message to Slack
    
    logger : logging.Logger
        logging object
    """
    channel_type = message["channel_type"]
    if channel_type == "im":
        # All types of message permitted in Apps channels
        pass
    
    else:
        if "thread_ts" not in message or "bot_id" in message:
            # Don't respond to non-mention if bot has not been mentioned before
            # or message is addressed to another bot
            return
        # Mentions are handled by handle_app_mention_events()
        mentions = re_get_mentions(message["text"])
        if mentions:
            return
    
    # ID for channel message received from
    # Set thread timestamp as channel ID 
    try:
        channel_id = message["thread_ts"]
    except KeyError:
        channel_id = message["ts"]
    
    # If no chain exists for this channel, create new one
    if not channel_id in THREADS_DICT:
        if channel_type == "im":
            build_chain(channel_id)
        else:
            # Don't join threads without mention
            return
    
    # Store user_message and get bot response
    bot_message = add_chain_link(channel_id, message, loc="apps")
    
    # Send generated response back in a thread
    thread_timestamp = message["ts"]
    say(bot_message, thread_ts = thread_timestamp)


@app.event(("app_mention"))
def handle_app_mention_events(body: dict, say: slack_bolt.Say, logger: logging.Logger) -> None:
    """
    Creates new chain when bot first mentioned
    
    Parameters
    ----------
    body : dict
        message received from Slack user in Channels
    
    say : slack_bolt.Say
        sends message to Slack
    
    logger : logging.Logger
        logging object
    """
    # Ignore mentions that don't include this bot
    mentions = re_get_mentions(body["event"]["text"])
    model = MODEL.split("/")[1]
    bot_id = MAP_MODEL_ID[model]
    if bot_id not in mentions:
        return
    
    # ID for channel message received from
    # Set thread timestamp as channel ID
    try:
        channel_id = body["event"]["thread_ts"]
    except KeyError:
        channel_id = body["event"]["ts"]
    
    # If no chain exists for this channel, create new one
    if not channel_id in THREADS_DICT:
        build_chain(channel_id)
        
    # Store user_message and get bot response
    bot_message = add_chain_link(channel_id, body, loc="mentions")

    # Send generated response back in a thread
    thread_timestamp = body["event"]["ts"]
    say(bot_message, thread_ts = thread_timestamp)


# ====================================
# Initialisation
# ====================================

if __name__ == "__main__":
    # Create an app-level token with connections:write scope
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

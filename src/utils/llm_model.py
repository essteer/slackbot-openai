# -*- coding: utf-8 -*-
import os, logging
import openai
from dotenv import load_dotenv

# Regex functions
from utils.regex import re_whitespace, re_user_prefixes, re_slack_id
# Constants
from utils.config import MODEL, MAX_TOKENS, TEMPERATURE, THREADS_DICT, TOP_P
from utils.system_prompt import SYSTEM_PROMPT
# Credentials
load_dotenv()
TOGETHER_API_KEY = os.environ["TOGETHER_API_KEY"]

logger = logging.getLogger(__name__)

# ====================================
# LLM Model
# ====================================

client = openai.OpenAI(
    api_key=TOGETHER_API_KEY, 
    base_url="https://api.together.xyz/v1"
)

# ====================================
# Conversation functions
# ====================================

def build_chain(thread_id: str) -> None:
    """
    Creates conversation chain upon first mention of bot
    Called by message_handler() and handle_app_mention_events()
    """
    memory = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Add memory to dict
    THREADS_DICT[thread_id] = memory
        

def add_chain_link(thread_id: str, msg: dict, loc: str) -> str:
    """
    Adds ConversationChain link for latest message round
    Called by message_handler() and handle_app_mention_events()
    """
    # Extract user message from Slack event
    if loc == "apps":
        msg_txt = re_whitespace(msg["text"])
    elif loc == "mentions":
        msg_txt = re_whitespace(msg["event"]["text"])
    
    # Clean messages with regex functions
    rgx_msg = re_slack_id(msg_txt)
    rgx_msg = re_whitespace(rgx_msg)
    rgx_msg = re_user_prefixes(rgx_msg)
    
    # Update memory with user message
    memory = THREADS_DICT[thread_id]
    memory.append({"role": "user", "content": rgx_msg})
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=memory,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            extra_body={"stop_token_ids": [7]}
        )
        
        bot_msg = response.choices[0].message.content
        # Clean messages with regex functions
        rgx_msg = re_slack_id(bot_msg)
        rgx_msg = re_whitespace(rgx_msg)
        rgx_msg = re_user_prefixes(rgx_msg)
        
        # Update memory with bot message
        memory.append({"role": "assistant", "content": rgx_msg})
        
        return rgx_msg
    
    except KeyError as e:
        logger.error(f"KeyError for THREADS_DICT: {e}")
        return "Something went wrong - please try again."
    

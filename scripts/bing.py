from urllib.parse import quote_plus
import os
import requests
from bs4 import BeautifulSoup

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session  # noqa

@simplebot.command()
def bing(bot: DeltaBot, message: Message, replies: Replies) -> 
None:
     """Send me any text in private to search in Bing"""
     if not replies.has_replies() and not message.chat.is_multiuser() and 
message.text:
         urls = _search(message.text)
         download_images(urls)
         replies.add(text="Images downloaded", quote=message)

def _search(query: str) -> list:
     query = query.replace("/wiki", "") 
     with session.get(f"https://www.bing.com/images/search?q={quote_plus(query)}&form=HDRSC2&first=1&tsc=ImageBasicHover") as resp:
         resp.raise_for_status()
         soup = BeautifulSoup(resp.text, 'html

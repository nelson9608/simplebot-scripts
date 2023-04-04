from urllib.parse import quote_plus
import os
import requests
from bs4 import BeautifulSoup

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session  # noqa

@simplebot.command()
def bing(bot: DeltaBot, message: Message, replies: Replies) -> None:
      """Send me any text in private to search in Bing"""
      if message.is_from_me() and message.is_private():
         urls = _search(message.text)
         download_images(urls)
         chat.send_text("Images downloaded", reply_to=message)

def _search(query: str) -> list:
     query = query.replace("/bing", "")
     with requests.Session() as session:
         resp = session.get(f"https://www.bing.com/images/search?q={quote_plus(query)}&form=HDRSC2&first=1&tsc=ImageBasicHover")
         resp.raise_for_status()
         soup = BeautifulSoup(resp.text, 'html.parser')
         urls = []
         for img in soup.find_all('img'):
             url = img.get('src')
             if url.startswith('http'):
                 urls.append(url)
         return urls

def download_images(urls: list):
     for url in urls:
         response = requests.get(url)
         filename = os.path.basename(url)
         with open(filename, 'wb') as f:
             f.write(response.content)

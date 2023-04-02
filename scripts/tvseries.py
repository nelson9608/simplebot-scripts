from urllib.parse import quote_plus

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session  # noqa


@simplebot.filter(trylast=True)
def search_filter(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Send me any text in private to search in the web."""
    if not replies.has_replies() and not message.chat.is_multiuser() and message.text:
        text, html = _search(bot.self_contact.addr, message.text)
        replies.add(text=text or "Search results", html=html, quote=message)
      
def _search(bot_addr: str, query: str) -> tuple:
     with session.get(f"https://www.imdb.com/find?q={quote_plus(query)}&s=tt&ttype=ft&ref_=fn_ft") as resp:
         resp.raise_for_status()
         soup = BeautifulSoup(resp.text, "html.parser")
         result = soup.find("td", class_="result_text")
         if result:
             link = result.find("a")["href"]
             with session.get(f"https://www.imdb.com{link}") as resp:
                 resp.raise_for_status()
                 soup = BeautifulSoup(resp.text, "html.parser")
                 summary = soup.find("div", class_="summary_text").get_text(strip=True)
                 return prepare_html(bot_addr, f"https://www.imdb.com{link}", summary)
         else:
             return prepare_html(bot_addr, resp.url, "No se encontraron resultados en IMDb.")

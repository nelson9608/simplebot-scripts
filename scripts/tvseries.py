from urllib.parse import quote_plus

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session  # noqa


@simplebot.command()
def sinopsis(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Send me the name of a TV series and I will send you a synopsis of it."""
    if not replies.has_replies() and not message.chat.is_multiuser() and message.text:
        text, html = _search(bot.self_contact.addr, message.text)
        replies.add(text=text or "Search results", html=html, quote=message)


def _search(bot_addr: str, query: str) -> tuple:
     query = query.replace("sinopsis", "")  # Elimina la palabra "sinopsis" 
del término de búsqueda
     with session.get(f"https://www.sensacine.com/busqueda/?q={quote_plus(query)}&cseries=1") 
as resp:
         resp.raise_for_status()
         return prepare_html(bot_addr, resp.url, resp.text)

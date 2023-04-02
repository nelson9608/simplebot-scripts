from urllib.parse import quote_plus

import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session  # noqa


@simplebot.command()
def wiki(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Send me any text in private to search in Wikipedia."""
    if not replies.has_replies() and not message.chat.is_multiuser() and message.text:
        text, html = _search(bot.self_contact.addr, message.text)
        replies.add(text=text or "Search results", html=html, quote=message)


def _search(bot_addr: str, query: str) -> tuple:
    with session.get(f"https://es.wikipedia.org/w/index.php?title=Special:Search&limit=20&offset=0&ns0=1&search={quote_plus(query)}") as resp:
        resp.raise_for_status()
        return prepare_html(bot_addr, resp.url, resp.text)

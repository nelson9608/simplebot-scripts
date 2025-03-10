"""
requirements:
simplebot_downloader
yt-dlp or youtube-dl
"""
import os
import time
from collections import OrderedDict
from threading import Thread
from typing import Callable, Dict, Generator

import simplebot

try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import MaxDownloadsReached
except ModuleNotFoundError:
    from youtube_dl import YoutubeDL
    from youtube_dl.utils import MaxDownloadsReached

from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_downloader.util import FileTooBig, get_setting, split_download  # noqa

MAX_QUEUE_SIZE = 20
downloads: Dict[str, Generator] = OrderedDict()


@simplebot.hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    Thread(target=_send_files, args=(bot,)).start()


@simplebot.command
def yt2video(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Download video from YouTube.

    Example:
    /yt2video https://www.youtube.com/watch?v=tZpxR8iM19s
    """
    queue_download(payload, bot, message, replies, download_ytvideo)


@simplebot.command
def yt2audio(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Download audio from YouTube video.

    Example:
    /yt2audio https://www.youtube.com/watch?v=tZpxR8iM19s
    """
    queue_download(payload, bot, message, replies, download_ytaudio)


def download_ytvideo(url: str, folder: str, max_size: int) -> str:
    opts = {
        "format": "18",
        "max_downloads": 1,
        "socket_timeout": 15,
        "outtmpl": os.path.join(folder, "%(id)s.%(ext)s"),
    }
    try:
        with YoutubeDL(opts) as yt:
            yt.download([url])
    except MaxDownloadsReached:
        pass
    return os.path.join(folder, os.listdir(folder)[0])

def download_ytaudio(url: str, folder: str, max_size: int) -> str:
    opts = {
        "format": f"bestaudio[filesize<?{max_size}]",
        "max_downloads": 1,
        "socket_timeout": 15,
        "outtmpl": os.path.join(folder, "%(id)s.%(ext)s"),
    }
    try:
        with YoutubeDL(opts) as yt:
            yt.download([url])
    except MaxDownloadsReached:
        pass
    return os.path.join(folder, os.listdir(folder)[0])


def queue_download(
    url: str,
    bot: DeltaBot,
    message: Message,
    replies: Replies,
    downloader: Callable,
) -> None:
    addr = message.get_sender_contact().addr
    if addr in downloads:
        replies.add(text="❌ You already have a download in queue", quote=message)
    elif len(downloads) >= MAX_QUEUE_SIZE:
        replies.add(
            text="❌ I'm too busy with too many downloads, try again later",
            quote=message,
        )
    else:
        replies.add(text="✔️ Request added to queue", quote=message)
        part_size = int(get_setting(bot, "part_size"))
        max_size = int(get_setting(bot, "max_size"))
        downloads[addr] = split_download(url, part_size, max_size, downloader)


def _send_files(bot: DeltaBot) -> None:
    replies = Replies(bot, bot.logger)
    while True:
        items = list(downloads.items())
        items = items and [items[0]]
        bot.logger.debug("Processing YouTube downloads queue (%s)", len(items))
        start = time.time()
        for addr, parts in items:
            chat = bot.get_chat(addr)
            try:
                path, num, parts_count = next(parts)
                replies.add(text=f"Part {num}/{parts_count}", filename=path, chat=chat)
                replies.send_reply_messages()
                if num == parts_count:
                    next(parts, None)  # close context
                    downloads.pop(addr, None)
            except FileTooBig as ex:
                downloads.pop(addr, None)
                replies.add(text=f"❌ {ex}", chat=chat)
                replies.send_reply_messages()
            except (StopIteration, Exception) as ex:
                bot.logger.exception(ex)
                downloads.pop(addr, None)
                replies.add(
                    text="❌ Failed to download file, is the link correct?", chat=chat
                )
                replies.send_reply_messages()
        delay = int(get_setting(bot, "delay")) - time.time() + start
        if delay > 0:
            tiempo _ dormir ( retraso)
          

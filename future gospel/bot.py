from tracemoe import TraceMoe

from os import getenv
from typing import Any

from hata import Client, Embed
from hata.ext import asyncio  # noqa: F401
from hata.ext.commands_v2 import cooldown

from dotenv import load_dotenv

load_dotenv("env")

rinie = Client(getenv("TOKEN"), extensions="commands_v2", prefix="!")


@rinie.events
async def ready(client):
    print("Bot has logged in.")


@rinie.commands
@cooldown("user", 5.0)
async def trace(client, message, url) -> Any:
    """
    This command looks up the anime frame and returns info around it.
    """
    url = url or (
        message.attachments[0].url if isinstance(message.attachments, tuple) else None
    )
    if url:
        tracemoe = TraceMoe(url, nsfw=message.channel.nsfw)
        return await tracemoe.search(embedify=True)
    else:
        return Embed(
            title="Error",
            description="Neither valid url nor an image attachment was found.",
            color=0x0000FF,
        )


rinie.start()

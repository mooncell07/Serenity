from tracemoe import TraceMoe

from os import getenv
from typing import Any

from hata import Client
from hata.ext import asyncio  # noqa: F401

from dotenv import load_dotenv

load_dotenv()


rinie = Client(getenv("TOKEN"), extensions="commands", prefix="!")


@rinie.events
async def ready(client):
    print("Bot has logged in.")


@rinie.commands
async def ping(client, message, url) -> Any:
    """
    This command looks up the anime frame and returns info around it.
    """
    tracemoe = TraceMoe(url)
    return await tracemoe.search(embedify=True)


rinie.start()

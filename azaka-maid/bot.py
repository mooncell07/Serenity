import logging
import os

import azaka
from dotenv import load_dotenv
from hata import Client
from hata.ext import asyncio  # noqa
from hata.ext.commands_v2 import cooldown
from embedder import vn_to_embed


logging.basicConfig(level=logging.DEBUG)
load_dotenv()

rinie = Client(os.getenv("TOKEN"), extensions="commands_v2", prefix="!")
client = azaka.Client(loop=rinie.loop)
azaka_future = rinie.loop.create_future()


async def main(ctx: azaka.Context, msg: str):
    result = await ctx.get_vn(lambda VN: VN.TITLE % msg, details=True)
    azaka_future.set_result(result)


@rinie.events
async def ready(client: Client) -> None:
    print("CONNECTED")


@rinie.commands
@cooldown(for_="user", reset=5.0, limit=3)
async def vn(msg: str):
    client.register(main, msg=msg)
    result = await azaka_future
    azaka_future.clear()

    return vn_to_embed(result[0])


rinie.start()
client.start()

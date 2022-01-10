import logging
import os

import azaka
from dotenv import load_dotenv
from hata import Client
from hata.ext import asyncio  # noqa

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

rinie = Client(os.getenv("TOKEN"), extensions="commands_v2", prefix="!")
client = azaka.Client(loop=rinie.loop)
azaka_future = rinie.loop.create_future()


async def main(ctx: azaka.Context, msg: str):
    result = await ctx.get_vn(lambda VN: VN.TITLE % msg)
    azaka_future.set_result(result)


@rinie.commands
async def vn(msg: str):
    client.register(main, msg=msg)
    result = await azaka_future
    azaka_future.clear()

    return result


rinie.start()
client.start()

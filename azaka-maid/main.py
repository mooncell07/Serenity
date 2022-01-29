import asyncio
import logging
import os
import typing as t

import azaka
from discord import DiscordException, Embed, Intents
from discord.ext import commands
from dotenv import load_dotenv

from embedder import vn_to_embed

logging.basicConfig(level=logging.DEBUG)
load_dotenv()


class Serenity(commands.Bot):
    __slots__ = ("results", "azaka_client")

    def __init__(self, **kwargs: t.Any) -> None:
        super().__init__(command_prefix=">", intents=Intents.all(), **kwargs)

        self.add_command(commands.Command(self.vn, name="vn"))

        # A queue for storing results from azaka.
        self.results: asyncio.Queue = asyncio.Queue()
        self.azaka_client: azaka.Client = azaka.Client(loop=self.loop)

    async def on_ready(self) -> None:
        print("CONNECTED TO DISCORD.")

    async def azaka_ready(self) -> None:
        # Newer version has `wait_until_connect`.
        await self.azaka_client._connector.on_connect.wait()
        print("CONNECTED TO VNDB.")

    async def get_vn(self, ctx: azaka.Context, title: str) -> None:
        """Internal method which makes call to the API and puts the
        result into a queue."""
        try:
            res = await ctx.get_vn(lambda VN: VN.TITLE % title, details=True)
        except azaka.AzakaException as exc:
            res = exc.message
        finally:
            await self.results.put(res)

    @commands.cooldown(rate=2, per=1, type=commands.BucketType.user)
    async def vn(self, ctx: commands.Context, *, title: str) -> t.Optional[Embed]:
        """A command to fetch VNs from VNDB."""
        self.azaka_client.register(self.get_vn, title=title)
        result = await self.results.get()
        if isinstance(result, list) and len(result) > 0:
            return await ctx.send(embed=vn_to_embed(result[0]))
        await ctx.send(result or "No results.")

    async def on_command_error(
        self, ctx: commands.Context, exc: DiscordException
    ) -> None:
        """Global Error Handler for discord.py exceptions."""
        if isinstance(exc, commands.CommandOnCooldown):
            await ctx.send("This command is on cooldown.")
        else:
            raise exc from None


serenity = Serenity()

# Not mandatory to install jishaku, just using it for personal use.
serenity.load_extension("jishaku")

serenity.loop.create_task(serenity.start(os.getenv("TOKEN")))
serenity.loop.create_task(serenity.azaka_ready())
serenity.azaka_client.start()

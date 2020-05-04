import json
import re
import asyncio
import filetype
import io
import aiohttp

from redbot.core import checks, Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify, inline


class Test(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.command()
    @checks.is_owner()
    async def test(self, ctx, *args):
        await ctx.send(str(args))

    @commands.command()
    @checks.is_owner()
    async def guesstype(self, ctx):
        for att in ctx.message.attachments:
            fp = io.FileIO("file", "w+")
            try:
                await att.save(fp, use_cached=True)
            except discord.errors.HTTPException:
                await att.save(fp)
            ft = filetype.is_image(fp)
            await ctx.send(ft)

    @commands.command()
    @checks.is_owner()
    async def mime(self, ctx, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                await ctx.send(resp.content_type)

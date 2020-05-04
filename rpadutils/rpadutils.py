import asyncio
import errno
import os
import re
import io
import signal
import filetype
from functools import wraps

import discord
from redbot.core import commands

RPADCOG = None

class RpadUtils(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

        global RPADCOG
        RPADCOG = self

    def user_allowed(self, message):
        author = message.author

        if author.bot:
            return False
        return True

def timeout_after(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


async def confirm_message(ctx, text, yemoji = "✅", nemoji = "❌", timeout = 10):
    msg = await ctx.send(text)
    await msg.add_reaction(yemoji)
    await msg.add_reaction(nemoji)
    def check(reaction, user):
        return (str(reaction.emoji) in [yemoji, nemoji]
                and user.id == ctx.author.id
                and reaction.message.id == msg.id)

    ret = False
    try:
        r, u = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
        if r.emoji == yemoji:
            ret = True
    except asyncio.TimeoutError:
        pass

    await msg.delete()
    return ret

def corowrap(coro, loop):
    def func(*args, **kwargs):
        fut = asyncio.run_coroutine_threadsafe(coro, loop)
        try:
            fut.result()
        except:
            pass
    return func

def fawait(coro, loop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        fut.result()
    except:
        pass

async def doubleup(ctx, message):
    lmessage = await ctx.history().__anext__()
    fullmatch = re.escape(message) + r"(?: x(\d+))?"
    match = re.match(fullmatch, lmessage.content)
    if match and lmessage.author == ctx.bot.user:
        n = match.group(1) or "1"
        await lmessage.edit(content=message+" x"+str(int(n)+1))
    else:
        await ctx.send(message)

async def isimage(fp: discord.Attachment):
    fp = io.FileIO(fp.filename, "w+")
    try:
        await att.save(fp, use_cached=True)
    except discord.errors.HTTPException:
        await att.save(fp)
    return filetype.is_image(fp)

async def saveimg(fp: io.BufferedIOBase):
    chan = RPADCOG.bot.get_channel(await RPADCOG.bot.get_cog("SBCore").config.savechan())
    return (await chan.send(file=discord.File(fp))).attachments[0].url

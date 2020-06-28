import re
import discord
import string
import random

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify, inline

from ABC import Splinter

def altCaps(s, up=True):
    o = ""
    for x in s:
        if up:
            o += x.upper()
        else:
            o += x.lower()
        if x in string.ascii_letters:
            up = not up
    return o

class WebhookEvent(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def proxy_message(self, message):
        try:
            if not isinstance(message.channel, discord.TextChannel):
                return
            fls = [await a.to_file() for a in message.attachments]
            for splinter_id in await self.bot.get_cog("SBCore").config.user(message.author).splinters():
                spl = await Splinter.fromId(splinter_id)
                fm = None
                for proxy in spl.proxies:
                    fm = re.fullmatch(re.escape(proxy).replace("text", "(.+)", 1), message.content)
                    if fm is not None:
                        break
                if fm is not None:
                    break
            else:
                return

            if not await self.bot.get_cog("Moderation").is_allowed(message.author, message.guild):
                await message.author.send(inline("You are not allowed to use splinters in that server."))
                return
            text = fm.group(1)

            for quirk in spl.quirks:
                text = text.replace(*quirk)

            for rquirk in spl.rquirks:
                if rquirk[1] == "$U":
                    rquirk = (rquirk[0], lambda x: x.group().upper())
                elif rquirk[1] == "$L":
                    rquirk = (rquirk[0], lambda x: x.group().lower())
                elif rquirk[1] == "$A":
                    rquirk = (rquirk[0], lambda x: altCaps(x.group()))
                elif rquirk[1] == "$A2":
                    rquirk = (rquirk[0], lambda x: altCaps(x.group(), False))
                elif re.match(r'rand\[.*[^\\]\]', rquirk[1]):
                    choices = rquirk[1]
                    rquirk = (rquirk[0], lambda x: random.choice(re.findall(r"rand\[(.*[^\\])\]", choices)[0].split('|')))

                text = re.sub(*rquirk, text)

            wid = await self.bot.get_cog("SBCore").config.channel(message.channel).webhook_id()
            webhook = discord.utils.get(await message.channel.webhooks(), id=wid)
            if not webhook:
                webhook = await message.channel.create_webhook(name="Polymorphic Splinter")
                wid = webhook.id
                await self.bot.get_cog("SBCore").config.channel(message.channel).webhook_id.set(wid)

            await webhook.send(
                content=text,
                username=spl.nick.get(str(message.guild.id), spl.name) + " - " + message.author.name,
                avatar_url=spl.avatar,
                files=fls,
            )
            await message.delete()
        except Exception as e:
            await message.channel.send("Error: {!r}".format(e))
            raise e

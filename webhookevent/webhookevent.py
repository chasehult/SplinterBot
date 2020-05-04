import re

from redbot.core import checks, Config
from redbot.core import commands

from ABC import Splinter

class WebhookEvent(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def proxy_message(self, message):
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
        text = fm.group(1)

        for quirk in spl.quirks:
            text = text.replace(*quirk)

        for rquirk in spl.rquirks:
            if rquirk[1] == "$U":
                rquirk = (rquirk[0], lambda x: x.group().upper())
            if rquirk[1] == "$L":
                rquirk = (rquirk[0], lambda x: x.group().lower())
            text = re.sub(*rquirk, text)

        wid = await self.bot.get_cog("SBCore").config.channel(message.channel).webhook_id()
        webhook = discord.utils.get(await message.channel.webhooks(), id = wid)
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

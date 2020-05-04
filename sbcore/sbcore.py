from redbot.core import checks, Config
from redbot.core import commands

from ABC import Splinter

class SBCore(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

        self.config = Config.get_conf(self, identifier=413612111111)
        self.config.register_user(splinters=[])  # List of IDs
        self.config.register_channel(webhook_id=None)
        self.config.register_global(splinters={}, cid=0, savechan=None)

    async def get_splinter(self, ctx, query, own=True):
        if own:
            sps = [await Splinter.fromId(sp) for sp in await self.config.user(ctx.author).splinters()]

            for sp in sps:
                if sp.name == query:
                    return sp
            for sp in sps:
                if sp.id == query:
                    return sp
            return None
        else:
            return Splinter.fromJson(await self.config.splinters().get(query))

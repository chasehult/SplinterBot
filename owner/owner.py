import discord

from redbot.core import checks, Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify, inline


class Owner(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    #@commands.command()
    @checks.is_owner()
    async def reset_all(self, ctx):
        await self.bot.get_cog("SBCore").config.clear_all()
        await ctx.send(inline("Done.  Everything has been reset."))

    @commands.command()
    @checks.is_owner()
    async def set_save_chan(self, ctx, savechan: discord.TextChannel):
        await self.bot.get_cog("SBCore").config.savechan.set(savechan.id)
        await ctx.send(inline("Done"))

    @commands.command()
    @checks.is_owner()
    async def freload(self, ctx, cmd, *, args=""):
        """Run a command after reloading its base cog."""
        full_cmd = "{}{} {}".format(ctx.prefix, cmd, args)
        cmd = self.bot.get_command(cmd)
        if cmd is None:
            await ctx.send("Invalid Command: {}".format(full_cmd))
            return
        await self.bot.get_cog("Core").reload(ctx, cmd.cog.__module__.split('.')[-1])
        ctx.message.content = full_cmd
        await self.bot.process_commands(ctx.message)

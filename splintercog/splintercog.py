import re
import io
import filetype
import aiohttp
import discord

from redbot.core import checks, Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify, inline

from rpadutils import rpadutils

from ABC import Splinter, SplinterACtx

class SplinterCog(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    @property
    def core(self):
        return self.bot.get_cog("SBCore")

    @commands.group(invoke_without_command=True)
    async def splinter(self, ctx, splinter, *, args=""):
        """The base group of all splinter related commands."""
        try:
            async with SplinterACtx(ctx, splinter) as spl:
                ctx.message.content = ctx.prefix + "splinter splinter_name " + args
                cctx = await self.bot.get_context(ctx.message)
                cctx.spec = spl
                await self.bot.invoke(cctx)
        except ValueError:
            await ctx.send("Invalid splinter name.")

    @splinter.command()
    async def add(self, ctx, *, name):
        """Adds a new splinter to your Ultimate Self."""
        newsp = await Splinter.new(name)
        async with self.core.config.user(ctx.author).splinters() as splinters:
            splinters.append(newsp.id)
        await newsp.save()
        msg = "Added {} (id: {}) to your Ultimate Self.".format(name, newsp.id)
        if re.search(r'\s', name):
            msg += ("\nNOTE: This splinter's name contains whitespace, so you'll need "
                    "to surround it with double quotes (\") when using commands referring "
                    "to it.")
        await ctx.send(box(msg))

    @splinter.command()
    async def remove(self, ctx, *, name):
        """Perminantly shatters a splinter from your Ultimate Self"""
        sp = await self.core.get_splinter(ctx, name.strip('"'))
        if sp is None:
            await ctx.send(inline("Unable to find splinter."))
            return
        if not rpadutils.confirm_message(ctx, "Are you sure you want to delete {} ({})".format(sp.name, sp.id)):
            await ctx.send("{} is still an active splinter.".format(sp.name))
        async with self.core.config.user(ctx.author).splinters() as splinters:
            splinters.remove(sp.id)
        await ctx.send(inline("{} has been perminantly shattered from your Ultimate Self".format(sp.name)))

    @splinter.command()
    async def list(self, ctx):
        """Lists the many splinters of your Ultimate Self"""
        msg = ""
        for sp in await self.core.config.user(ctx.author).splinters():
            sp = Splinter.fromId(sp)
            msg += "{} ({})\n".format(sp.name, sp.id)
        if not msg:
            await ctx.send(inline("Your current self is whole.  Try adding a splinter."))
        for page in pagify(msg):
            await ctx.send(box(page))

    @splinter.group()
    @commands.check(lambda ctx: hasattr(ctx, "spec"))
    async def splinter_name(self, ctx):
        pass

    @splinter_name.command(aliases=["getid"])
    async def id(self, ctx, *, id_error = None):
        """Gets a splinter's ID"""
        if id_error:
            await ctx.send(inline("You cannot set a splinter's ID."))
            return
        await ctx.send(inline(ctx.spec.id))

    @splinter_name.command(aliases=["setnick", "delnick", "rmnick"])
    async def nick(self, ctx, *, nick = None):
        """Sets or removes a splinter's nickname."""
        ctx.spec.nick[ctx.guild.id] = nick
        await ctx.send(inline("Done"))

    @splinter_name.command(aliases=["setcolor"])
    async def color(self, ctx, *, color: discord.Color):
        """Sets or removes a splinter's color."""
        ctx.spec.color = color.value
        await ctx.send(inline("Done"))

    @splinter_name.command(aliases=["setavatar"])
    async def avatar(self, ctx, *, avatar = None):
        """Sets or removes a splinter's avatar."""
        if ctx.message.attachments:
            fp = io.FileIO(ctx.message.attachments[0].filename, "w+")
            try:
                await ctx.message.attachments[0].save(fp, use_cached=True)
            except discord.errors.HTTPException:
                await ctx.message.attachments[0].save(fp)
            if not filetype.is_image(fp):
                await ctx.send(inline("The attached file must be an image."))
                return
            fp.seek(0)
            ctx.spec.avatar = await rpadutils.saveimg(fp)
        elif avatar is None:
            await ctx.send(ctx.spec.avatar or inline("You do not have an avatar set."))
            return
        elif avatar.lower() in ["clear", "none", "remove"]:
            ctx.spec.avatar = None
        else:
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(avatar) as resp:
                        if not resp.content_type.split("/")[0] == "image":
                            await ctx.send(inline("The attatched link must be an image."))
                            return
                        fp = io.FileIO("image."+resp.content_type.split("/")[1], "w+")
                        fp.write(await resp.read())
                        fp.seek(0)
                        ctx.spec.avatar = await rpadutils.saveimg(fp)
                except (aiohttp.client_exceptions.InvalidURL, AssertionError):
                    await ctx.send(inline("That's an invalid URL."))
                    return

        await ctx.send(inline("Done"))

    @splinter_name.group(aliases=["quirks", "getquirks"], invoke_without_command=True, ignore_extra=False)
    async def quirk(self, ctx):
        """Manage a splinter's quirks."""
        msg = ""
        for c, quirk in enumerate(ctx.spec.quirks):
            msg += "{2})  {0!r}\n    to\n    {1!r}\n\n".format(*quirk, c+1)
        for page in pagify(msg):
            await ctx.send(box(page))

    @quirk.command(name="add")
    async def quirk_add(self, ctx, fr, to, *, error=None):
        if error is not None:
            await ctx.send(inline("Too many arguments.  Make sure to surround both"
                           "arguments with double quotes (\")."))
            return
        ctx.spec.quirks.append((fr, to))
        await ctx.send(box("Added quirk:\n{!r}\nto\n{!r}".format(fr, to)))

    @quirk.command(name="list")
    async def quirk_list(self, ctx):
        await self.quirk(ctx)

    @quirk.command(name="remove", aliases=["delete"])
    async def quirk_remove(self, ctx, index: int):
        if index > len(ctx.spec.quirks) or index < 1:
            await ctx.send(inline("That's not a valid quirk index."))
            return
        qiq = ctx.spec.quirks[index-1]
        if await rpadutils.confirm_message(ctx, inline("Are you sure you want to delete the "
                                            "quirk:\n{!r}\nto\n{!r}").format(*qiq)):
            ctx.spec.quirks.pop(index-1)


    @splinter_name.group(aliases=["rquirks", "getrquirks"], invoke_without_command=True, ignore_extra=False)
    async def rquirk(self, ctx):
        """Manage a splinter's regex quirks."""
        msg = ""
        for c, rquirk in enumerate(ctx.spec.rquirks):
            msg += "{})  r'{}'\n    to\n    r'{}'\n\n".format(c+1, *rquirk)
        for page in pagify(msg):
            await ctx.send(box(page))

    @rquirk.command(name="add")
    async def rquirk_add(self, ctx, fr, to, *, error=None):
        if error is not None:
            await ctx.send(inline("Too many arguments.  Make sure to surround both"
                           "arguments with double quotes (\")."))
            return
        try:
            re.sub(fr, to, "")
        except re.error:
            await ctx.send(inline("Invalid regex."))
        ctx.spec.rquirks.append((fr, to))
        await ctx.send(box("Added regex quirk:\nr'{}'\nto\nr'{}'".format(fr, to)))

    @rquirk.command(name="list")
    async def rquirk_list(self, ctx):
        await self.rquirk(ctx)

    @rquirk.command(name="remove", aliases=["delete"])
    async def rquirk_remove(self, ctx, index: int):
        if index > len(ctx.spec.rquirks) or index < 1:
            await ctx.send(inline("That's not a valid regex quirk index."))
            return
        qiq = ctx.spec.rquirks[index-1]
        if await rpadutils.confirm_message(ctx, inline("Are you sure you want to delete the "
                                            "regex quirk:\nr'{}'\nto\nr'{}'").format(*qiq)):
            ctx.spec.rquirks.pop(index-1)


    @splinter_name.group(aliases=["proxies", "getproxies", "getproxy"], invoke_without_command=True, ignore_extra=False)
    async def proxy(self, ctx):
        """Manage a splinter's proxies."""
        msg = ""
        for c, proxy in enumerate(ctx.spec.proxies):
            msg += "{})\t{}\n".format(c+1, proxy)
        for page in pagify(msg):
            await ctx.send(box(page))

    @proxy.command(name="add")
    async def proxy_add(self, ctx, *, proxy):
        if "text" not in proxy:
            await ctx.send(inline("Your proxy must have the word 'text' in it."))
            return
        ctx.spec.proxies.append(proxy)
        await ctx.send(inline("Done"))

    @proxy.command(name="list")
    async def proxy_list(self, ctx):
        await self.proxy(ctx)

    @proxy.command(name="remove", aliases=["delete"])
    async def proxy_remove(self, ctx, index: int):
        if index > len(ctx.spec.proxies) or index < 1:
            await ctx.send(inline("That's not a valid proxy index."))
            return
        piq = ctx.spec.proxies[index-1]
        if await rpadutils.confirm_message(ctx, inline("Are you sure you want to delete the "
                                                  "proxy:\n{}").format(piq)):
            ctx.spec.proxies.pop(index-1)

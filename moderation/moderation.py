import discord

from redbot.core import checks
from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import inline, box, pagify

old_blacklist = old_whitelist = None

class Moderation(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(self, identifier=413612111111)

        self.config.register_guild(
            blacklist={'active':True, 'users':[],'roles':[]},
            whitelist={'active':False, 'users':[],'roles':[]}
        )

    def cog_unload(self):
        global old_blacklist, old_whitelist
        if old_blacklist:
            try:     self.bot.remove_command("blacklist")
            except:  pass
            self.bot.add_command(old_blacklist)
        if old_whitelist:
            try:     self.bot.remove_command("whitelist")
            except:  pass
            self.bot.add_command(old_whitelist)

    @commands.group()
    @checks.mod_or_permissions(manage_guild=True)
    async def blacklist(self, ctx):
        """Manage blacklisted roles and users"""

    @blacklist.command(name="add")
    async def blacklist_add(self, ctx, role_or_user):
        """Add a role or user to the blacklist"""
        try:
            role = await commands.RoleConverter().convert(ctx, role_or_user)
            async with self.config.guild(ctx.guild).blacklist() as blacklist:
                blacklist['roles'].append(role.id)
            await ctx.send(inline("Added role '{}' to the blacklist.".format(role.name)))
        except commands.CommandError:
            user = await commands.MemberConverter().convert(ctx, role_or_user)
            async with self.config.guild(ctx.guild).blacklist() as blacklist:
                blacklist['users'].append(user.id)
            await ctx.send(inline("Added user '{}' to the blacklist.".format(user.name)))

    @blacklist.command(name="remove")
    async def blacklist_remove(self, ctx, role_or_user):
        """Remove a role or user from the blacklist"""
        try:
            role = await commands.RoleConverter().convert(ctx, role_or_user)
            removed = False
            async with self.config.guild(ctx.guild).blacklist() as blacklist:
                if role.id in blacklist['roles']:
                    blacklist['roles'].remove(role.id)
                    removed = True
            if removed:
                await ctx.send(inline("Removed role '{}' from the blacklist.".format(role.name)))
            else:
                await ctx.send(inline("Role '{}' is not blacklisted.".format(role.name)))
        except commands.CommandError:
            user = await commands.MemberConverter().convert(ctx, role_or_user)
            removed = False
            async with self.config.guild(ctx.guild).blacklist() as blacklist:
                if user.id in blacklist['users']:
                    blacklist['users'].remove(user.id)
                    removed = True
            if removed:
                await ctx.send(inline("Removed user '{}' from the blacklist.".format(user.name)))
            else:
                await ctx.send(inline("User '{}' is not blacklisted.".format(user.name)))

    @blacklist.command(name="clear")
    async def blacklist_clear(self, ctx, role_or_user):
        """Clear the blacklist"""
        async with self.config.guild(ctx.guild).blacklist() as blacklist:
            blacklist['users'] = []
            blacklist['roles'] = []
        await ctx.send(inline("Done"))

    @blacklist.command(name="list")
    async def blacklist_list(self, ctx):
        """Lists all roles and users on the blacklist"""
        async with self.config.guild(ctx.guild).blacklist() as blacklist:
            msg = "Roles:\n"
            for rid in blacklist['roles'][:]:
                role = ctx.guild.get_role(rid)
                if role is None:
                    blacklist['roles'].remove(rid)
                    continue
                msg += role.name + "\n"
            msg+="\nUsers:\n"
            for mid in blacklist['users'][:]:
                user = ctx.guild.get_member(mid)
                if user is None:
                    # blacklist['users'].remove(mid)
                    continue
                msg += user.name + "\n"

        for page in pagify(msg):
            await ctx.send(box(page))

    @blacklist.command(name="toggle")
    async def blacklist_toggle(self, ctx, to: bool = None):
        """Turns blacklisting on or off"""
        async with self.config.guild(ctx.guild).blacklist() as blacklist:
            if to is None:
                blacklist['active'] = not blacklist['active']
            else:
                blacklist['active'] = to
            await ctx.send(inline("The blacklist is now turned " + ("on" if blacklist['active'] else "off")))


    @commands.group()
    @checks.mod_or_permissions(manage_guild=True)
    async def whitelist(self, ctx):
        """Manage whitelisted roles and users."""

    @whitelist.command(name="add")
    async def whitelist_add(self, ctx, role_or_user):
        """Add a role or user to the whitelist"""
        try:
            role = await commands.RoleConverter().convert(ctx, role_or_user)
            async with self.config.guild(ctx.guild).whitelist() as whitelist:
                whitelist['roles'].append(role.id)
            await ctx.send(inline("Added role '{}' to the whitelist.".format(role.name)))
        except commands.CommandError:
            user = await commands.MemberConverter().convert(ctx, role_or_user)
            async with self.config.guild(ctx.guild).whitelist() as whitelist:
                whitelist['users'].append(user.id)
            await ctx.send(inline("Added user '{}' to the whitelist.".format(user.name)))

    @whitelist.command(name="remove")
    async def whitelist_remove(self, ctx, role_or_user):
        """Remove a role or user from the whitelist"""
        try:
            role = await commands.RoleConverter().convert(ctx, role_or_user)
            removed = False
            async with self.config.guild(ctx.guild).whitelist() as whitelist:
                if role.id in whitelist['roles']:
                    whitelist['roles'].remove(role.id)
                    removed = True
            if removed:
                await ctx.send(inline("Removed role '{}' from the whitelist.".format(role.name)))
            else:
                await ctx.send(inline("Role '{}' is not whitelisted.".format(role.name)))
        except commands.CommandError:
            user = await commands.MemberConverter().convert(ctx, role_or_user)
            removed = False
            async with self.config.guild(ctx.guild).whitelist() as whitelist:
                if user.id in whitelist['users']:
                    whitelist['users'].remove(user.id)
                    removed = True
            if removed:
                await ctx.send(inline("Removed user '{}' from the whitelist.".format(user.name)))
            else:
                await ctx.send(inline("User '{}' is not whitelisted.".format(user.name)))

    @whitelist.command(name="clear")
    async def whitelist_clear(self, ctx, role_or_user):
        """Clear the whitelist"""
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            whitelist['users'] = []
            whitelist['roles'] = []
        await ctx.send(inline("Done"))

    @whitelist.command(name="list")
    async def whitelist_list(self, ctx):
        """List all roles and users on the whitelist"""
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            msg = "Roles:\n"
            for rid in whitelist['roles'][:]:
                role = ctx.guild.get_role(rid)
                if role is None:
                    whitelist['roles'].remove(rid)
                    continue
                msg += role.name + "\n"
            msg+="\nUsers:\n"
            for mid in whitelist['users'][:]:
                user = ctx.guild.get_member(mid)
                if user is None:
                    # whitelist['users'].remove(mid)
                    continue
                msg += user.name + "\n"

        for page in pagify(msg):
            await ctx.send(box(page))

    @whitelist.command(name="toggle")
    async def whitelist_toggle(self, ctx, to: bool = None):
        """Turns whitelisting on or off"""
        async with self.config.guild(ctx.guild).whitelist() as whitelist:
            if to is None:
                whitelist['active'] = not whitelist['active']
            else:
                whitelist['active'] = to
            await ctx.send(inline("The whitelist is now turned " + ("on" if whitelist['active'] else "off")))



    async def is_allowed(self, member, guild):
        blacklist = await self.config.guild(guild).blacklist()
        whitelist = await self.config.guild(guild).whitelist()

        if blacklist['active']:
            if member.id in blacklist['users'] or {role.id for role in member.roles} & set(blacklist['roles']):
                return False
        if whitelist['active']:
            if member.id not in whitelist['users'] or not ({role.id for role in member.roles} & set(whitelist['roles'])):
                return False
        return True



def csetup(bot):
    global old_blacklist, old_whitelist
    old_blacklist = bot.get_command("blacklist")
    if old_blacklist:
        bot.remove_command(old_blacklist.name)

    old_whitelist = bot.get_command("whitelist")
    if old_whitelist:
        bot.remove_command(old_whitelist.name)
    bot.add_cog(Moderation(bot))

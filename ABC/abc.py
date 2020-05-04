import json
import string
import contextlib

from redbot.core import checks, Config
from redbot.core import commands

ABCog = None

class ABC(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

        global ABCog
        ABCog = self

    async def next_id(self):
        ocid = cid = await self.bot.get_cog("SBCore").config.cid() % (26**5)
        id = ""
        for i in range(5):
            cid, ch = divmod(cid, 26)
            id = string.ascii_uppercase[ch] + id
        await self.bot.get_cog("SBCore").config.cid.set(ocid+4133)
        return id


class Splinter:
    def __init__(self, id, name, nick, proxies, color, avatar, quirks, rquirks):
        self.name = name
        self.id = id
        self.nick = nick
        self.proxies = proxies
        self.color = color
        self.avatar = avatar
        self.quirks = quirks
        self.rquirks = rquirks

    @staticmethod
    async def new(name):
        return Splinter(**{
            'id': await ABCog.next_id(),
            'name': name,
            'nick': {},
            'proxies': [],
            'color': 0x99aab5,
            'avatar': None,
            'quirks': [],  # (from, to)
            'rquirks': [], # (from, to)
        })

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'nick': self.nick,
            'proxies': self.proxies,
            'color': self.color,
            'avatar': self.avatar,
            'quirks': self.quirks,
            'rquirks': self.rquirks,
        })

    @staticmethod
    def fromJson(payload):
        return Splinter(**json.loads(payload))


    @staticmethod
    async def fromId(id):
        newsp = (await ABCog.bot.get_cog("SBCore").config.splinters()).get(id)
        if newsp is None:
            return None
        return Splinter.fromJson(newsp)

    async def save(self):
        async with ABCog.bot.get_cog("SBCore").config.splinters() as splinters:
            splinters[self.id] = self.toJson()

    def __eq__(self, other):
        if isinstance(other, Splinter):
            return other.id == self.id
        elif isinstance(other, str):
            try:
                return Splinter.fromJson(other).id == self.id
            except:
                return False

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class SplinterACtx(contextlib.AbstractAsyncContextManager):
    def __init__(self, ctx, query):
        self.ctx = ctx
        self.query = query
        self.splinter = None

    async def __aenter__(self):
        self.splinter = await ABCog.bot.get_cog("SBCore").get_splinter(self.ctx, self.query)
        if self.splinter is None:
            raise ValueError("Invalid query: "+self.query)
        return self.splinter

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.splinter.save()

from redbot.core import checks, Config
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify, inline


class Homestuck(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

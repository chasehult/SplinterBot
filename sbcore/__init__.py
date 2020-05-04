from .sbcore import SBCore

def setup(bot):
    bot.add_cog(SBCore(bot))

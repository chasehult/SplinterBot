from .webhookevent import WebhookEvent

def setup(bot):
    bot.add_cog(WebhookEvent(bot))

from discord.ext.commands import Cog
from discord.ext.commands import command


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="cmd", aliases=["command", "c"], hidden=True)
    async def somecommand(self, ctx):
        await ctx.send("cmd successdully creatred")

    @Cog.listener()
    async def on_ready(self):
        await self.bot.CHANNEL.send('fun cog Connected and ready')
        print('fun cog ready')


def setup(bot):
    bot.add_cog(Fun(bot))

from discord.ext.commands import Cog
from discord.ext.commands import command


class Teams(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="cmd2", aliases=["command2", "c2"], hidden=True)
    async def somecommand2(self, ctx):
        await ctx.send("cmd2 successdully creatred")

    @Cog.listener()
    async def on_ready(self):
        await self.bot.CHANNEL.send('Teams cog Connected and ready')
        print('Teams cog ready')


def setup(bot):
    bot.add_cog(Teams(bot))

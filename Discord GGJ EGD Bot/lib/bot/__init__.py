import os
import random
from datetime import datetime
from discord.ext.commands.errors import CommandNotFound
from discord.flags import Intents
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from glob import glob


PREFIX = "!"
OWNER_IDS = [134725225140060160]
#COGS = [path.split("\\")[-1][:3] for path in glob("./lib/cogs/*.py")]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
print(COGS)


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.schedulers = AsyncIOScheduler()
        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            Intents=Intents.all()
        )

    def run(self, version):
        load_dotenv()
        self.VERSION = version
        self.TOKEN = os.getenv('DISCORD_TOKEN')

        print('setup bot')
        self.setup()

        print('running bot')
        super().run(self.TOKEN, reconnect=True)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded")
        print('setup completed')

    async def on_connect(self):
        print('bot connected')

    async def on_disconnect(self):
        print('bot disconnected')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrongs")
        raise  # type:ignore

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send('Wrong command')
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def print_msg(self):
        await self.CHANNEL.send("TIMED")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print('bot ready')
            #self.guild = self.get_guild(os.getenv('GUILD_ID'))
            self.CHANNEL = self.get_channel(785813944140169231)
            await self.CHANNEL.send("Connected")

            # self.schedulers.add_job(
            #     self.print_msg, CronTrigger(second="0,15,30,45"))
            # self.schedulers.start()

            # embed = Embed(title='Hello', description='ENJOY PLEASE!',
            #               colour=0x00CC00, timestamp=datetime.utcnow())
            # field = [("Name", "Value", True),
            #          ("Another field", "Another value", True),
            #          ("a non inline field", "this will appear in it's own row", True),
            #          ("Another field", "Another value", True),
            #          ("Name", "Value", True)]
            # for name, value, inline in field:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_footer(text="test")
            # embed.set_author(
            #     name="Mickey", icon_url='https://i.pinimg.com/originals/a7/80/d8/a780d8f211dfdae66dacf9547e45fbbc.jpg')
            # embed.set_thumbnail(
            #     url='https://i.pinimg.com/originals/a7/80/d8/a780d8f211dfdae66dacf9547e45fbbc.jpg')
            # embed.set_image(
            #     url='https://i.pinimg.com/originals/a7/80/d8/a780d8f211dfdae66dacf9547e45fbbc.jpg')
            # await self.CHANNEL.send(embed=embed)
        else:
            print('bot reconnected')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()

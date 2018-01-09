
import modules.functions as funcs
import config, discord, discord.ext.commands.errors, asyncio
from discord.ext import commands

DESCRIPTION = "An Elimere bot that really doesn't like to be asked questions!"
BOT_PREFIX = "$eli "


INITIAL_EXTENSIONS = (
    'modules.errorhandling',
    'modules.commands'
)


def RunBot():
    bot = ElimereBot()
    bot.run()


class ElimereBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=BOT_PREFIX, description=DESCRIPTION, pm_help=None, help_attrs=dict(hidden=True))
        self.guild_only = True
        self.bg_task = self.loop.create_task(self.BackgroundLogCheck())

        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
                print(f'Loaded {extension} extension')
            except Exception as e:
                print(e)
                print(f'Failed to load extension {extension}')

    async def on_ready(self):
        print('-------------')
        print('Logged in as: ' + self.user.name)
        print('Bot ID: ' + str(self.user.id))
        print('Discord.py Version: ' + str(discord.__version__))
        print('-------------')

    async def BackgroundLogCheck(self):
        """This checks the current date"""
        await self.wait_until_ready()
        channel = self.get_guild(config.guildServerID).get_channel(config.guildLogChanID)
        while not self.is_closed():
            msg = await funcs.CheckForLogs()
            if msg != "":
                await channel.send(msg)
            await asyncio.sleep(600)

    async def on_message(self, message):
        message.content = message.content.lower()
        if await funcs.CheckForString(message):
            message.content = "$eli BotRespond"
            await self.process_commands(message)
        else:
            await self.process_commands(message)

    def run(self):
        super().run(config.token)





RunBot()

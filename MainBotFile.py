
import config
import discord
import discord.ext.commands.errors
from discord.ext import commands

DESCRIPTION = "An Elimere bot that really doesn't like to be asked questions!"
BOT_PREFIX = "$eli "


INITIAL_EXTENSIONS = (
    'modules.errorhandling',
    'modules.commands'
)

#
def RunBot():
    bot = ElimereBot()
    bot.run()

class ElimereBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=BOT_PREFIX, description=DESCRIPTION, pm_help=None, help_attrs=dict(hidden=True))
        self.guild_only = True

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

    async def on_message(self, message):
        message.content = str(message.content.lower())
        await self.process_commands(message)

    def run(self):
        super().run(config.token)

RunBot()

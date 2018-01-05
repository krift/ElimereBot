#pylint: disable = W, C

import discord
import discord.ext.commands.errors

from discord.ext.commands import Bot
from discord.ext import commands

description = "An Elimere bot that really doesn't like to be asked questions!"
bot_prefix = "!Elimere"

def RunBot():
    bot = ElimereBot()
    bot.run()

class ElimereBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=bot_prefix, description=description, pm_help=none, help_attrs=dict(hidden=true))
        self.guild_only = True

    async def on_ready(self):
        print('-------------')
        print('Logged in as: ' + self.user.name)
        print('Bot ID: ' + str(self.user.id))
        print('Discord.py Version: ' + str(discord.__version__))
        print('-------------')

    async def on_message(self, message):
        await self.process_commands(message)

    def run(self):
        super().run("Bot Token goes here.")

RunBot()

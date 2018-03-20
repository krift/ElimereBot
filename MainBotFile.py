#!/usr/local/bin/python3.6
import modules.functions as funcs
import config
import discord
import discord.ext.commands.errors
import botoptions
import datetime
import traceback
from discord.ext import commands

DESCRIPTION = "An Elimere bot that really doesn't like to be asked questions!"
BOT_PREFIX = "$eli "


INITIAL_EXTENSIONS = (
    'modules.errorhandling',
    'modules.commands',
    'modules.dev',
    'modules.warcraftlogs',
    'modules.raiderio'
)


def RunBot():
    bot = ElimereBot()
    bot.run()


class ElimereBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=BOT_PREFIX, description=DESCRIPTION, pm_help=None, help_attrs=dict(hidden=True))
        self.guild_only = True

        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)  # Load the extension, so you don't have to import it
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

    async def on_member_join(self, member):  # This is fired every time a user joins a server with this bot on it
        channel = self.get_guild(config.guildServerID).get_channel(config.guildGenChanID)  # Select the top most text channel in the server
        # Send this message
        await channel.send("Hello "+member.mention+"! Hope you enjoy your stay here! We're all happy you decided to join us!")

    async def on_message(self, message):
        if message.embeds:
            if message.author.name == "GitHub":
                embeds = message.embeds[0].to_dict()
                if embeds['title'].lower().rfind('elimerebot:master') != -1:
                    message.content = '$eli PullUpdate'
                    await self.process_commands(message)
        if message.author.bot is False:  # So the bot won't process bot messages
            if message.content == '':
                return
            if message.content[0] == '$':  # If the message is actually a command, process it
                await self.process_commands(message)  # This part processes the actual command
                return  # Return so it doesn't run any other part of this
            response = await funcs.CheckResponseString(botoptions.eli_main_responses, message)  # Check to see if it's a keyword
            god_response = await funcs.CheckResponseString(botoptions.god_responses, message) # Checks if a keyword from the gods
            if god_response != '':
                if (message.author.id == 167419045128175616) is not (message.author.id == 198574477347520513):
                    # If either author is the devs
                    message.content = god_response  # Send a god response
                    await message.channel.send(message.content)
            elif response != '':  # Else, send a normal response
                message.content = response
                await message.channel.send(message.content)
            elif await funcs.CheckForString(message):  # If it's not a keyword, run the BotRespond command
                message.content = "$eli BotRespond"
                await self.process_commands(message)

    def run(self):
        super().run(config.token)

    async def on_error(self, event, *args, **kwargs):
        """Default error handler"""
        e = discord.Embed(title="Event Error", colour=0x32952)
        e.add_field(name="Event", value=event)
        e.add_field(name="args", value=str(args))
        e.add_field(name="kwargs", value=str(kwargs))
        e.description = f'```py\n{traceback.format_exc()}\n```'
        e.timestamp = datetime.datetime.utcnow()
        await self.get_guild(config.devServerID).get_channel(config.errorChanID).send(embed=e)


RunBot()

#!/usr/local/bin/python3.6
import modules.functions as funcs
import config
import discord
import discord.ext.commands.errors
import botoptions
import datetime
import traceback
import git
import subprocess
import os
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

    async def on_ready(self): # This fires once the bot has connected
        print('-------------')
        print('Logged in as: ' + self.user.name)
        print('Bot ID: ' + str(self.user.id))
        print('Discord.py Version: ' + str(discord.__version__))
        print('-------------')
        self.check_for_update()


    async def on_member_join(self, member):  # This is fired every time a user joins a server with this bot on it
        channel = self.get_guild(config.guildServerID).get_channel(config.guildGenChanID)  # Select the top most text channel in the server
        # Send this message
        await channel.send("Hello "+member.mention+"! Hope you enjoy your stay here! We're all happy you decided to join us!")

    async def on_message(self, message):
        try:
            if message.embeds: # If the message sent was an embed
                if message.author.name == "GitHub": # If the author is the github bot
                    embeds = message.embeds[0].to_dict() # Look to see if the branch is the master branch then pull the new update
                    if embeds['title'].lower().rfind('elimerebot:master') != -1:
                        message.content = '$eli PullUpdate'
                        await self.process_commands(message)
                        return

            if message.author.bot is False:  # So the bot won't process bot messages
                if message.content.rfind(config.secretID) != -1:
                    if datetime.datetime.now().hour < 14:
                        await self.get_guild(message.guild.id).get_channel(message.channel.id).send(
                            botoptions.no_tag_please)
                if message.content == '':
                    return
                if message.content[0] == '$':  # If the message is actually a command, process it
                    await self.process_commands(message)  # This part processes the actual command
                    return  # Return so it doesn't run any other part of this
                response = await funcs.CheckResponseString(botoptions.eli_main_responses, message)  # Check to see if it's a keyword
                god_response = await funcs.CheckResponseString(botoptions.god_responses, message) # Checks if a keyword from the gods
                if god_response != '':
                    if self.check_dev(message.author.id):
                        # If either author is the devs
                        message.content = god_response  # Send a god response
                        await message.channel.send(message.content)
                elif response != '':  # Else, send a normal response
                    message.content = response
                    await message.channel.send(message.content)
                elif await funcs.CheckForString(message):  # If it's not a keyword, run the BotRespond command
                    message.content = "$eli BotRespond"
                    await self.process_commands(message)
        except AttributeError as e:
            await self.get_guild(config.devServerID).get_channel(config.errorChanID).send(e.__str__() + " in server " + str(message.guild))
            return

    def check_dev(self, id):
        """Checks whether the passed ID matches"""
        return id == 167419045128175616 or id == 167419045128175616

    def check_for_update(self):
        """Checks to see if the local repo is different and then updates"""
        local_repo = git.Repo(search_parent_directories=True)
        local_sha = local_repo.head.object.hexsha
        # local_short_sha = local_repo.git.rev_parse(local_sha)
        remote_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=local_repo.git_dir).decode(
            'ascii').strip()
        if local_sha != remote_sha:
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            g = git.cmd.Git(path)
            g.pull()
            os.system('sudo systemctl restart elimerebot.service')

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

from datetime import datetime
from discord.ext import commands
import config
import botoptions
import datetime
import traceback
import asyncio
import logging, logging.config
import modules.wow.wowhead as wow

DESCRIPTION = "An Elimere bot that really doesn't like to be asked questions!"
BOT_PREFIX = "$eli "


INITIAL_EXTENSIONS = (
    'modules.botsetups',
    'modules.tags',
    'modules.commands',
    'modules.wow.warcraftlogs',
    'modules.wow.raiderio',
    'modules.roles',
    'modules.errorhandling',
    'modules.dev'
)


# noinspection PyPep8Naming
def RunBot():
    bot = ElimereBot()
    bot.run()


class ElimereBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=BOT_PREFIX, description=DESCRIPTION, pm_help=False, help_attrs=dict(hidden=True))
        self.guild_only = True
        self.event_loop = asyncio.get_event_loop()
        b = wow.Wowhead(self)
        self.event_loop.create_task(b.ensure_option_exists())
        self.event_loop.create_task(self.check_articles())
        self.event_loop.create_task(self.check_for_logs())

        for extension in INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
                print(f'Loaded {extension} extension')
            except Exception as e:
                print(e)
                print(f'Failed to load extension {extension}')

    async def on_ready(self):
        pass

    async def check_articles(self):
        """
        This function creates a new Wowhead reference and runs the post_new_article function.
        """
        await asyncio.sleep(5)
        a = wow.Wowhead(self)
        for server in self.guilds:
            await a.post_new_article(str(server.id))
            await asyncio.sleep(1)
        await asyncio.sleep(25)
        del a
        await asyncio.sleep(300)
        self.event_loop.create_task(self.check_articles())

    async def check_for_logs(self):
        """
        This function creates a new WarcraftLogs reference and runs the auto_pull_log function.
        """
        await asyncio.sleep(5)
        b = self.get_cog('WarcraftLogs')
        for server in self.guilds:
            await b.auto_pull_log(str(server.id))
            await asyncio.sleep(1)
        await asyncio.sleep(25)
        del b
        await asyncio.sleep(300)
        self.event_loop.create_task(self.check_for_logs())

    # async def on_member_join(self, member):  # This is fired every time a user joins a server
    #     channel = self.get_guild(config.guildServerID).get_channel(config.guildGenChanID)  # Select the top most text channel in the server
    #     # Send this message
    #     await channel.send("Hello "+member.mention+"! Hope you enjoy your stay here! We're all happy you decided to join us!")

    async def on_message(self, message):
        async def check_for_string(msg):
            """Checks the message to see if it matches the hey eli strings"""
            for string in botoptions.hey_eli:  # For each string in hey_eli list
                if msg.content.lower().rfind(string) != -1:  # If it is found, return True
                    return True

        async def check_response_string(response_dict, msg):
            """This checks a dictionary of strings and returns appropriately"""
            for key in response_dict.keys():  # This looks at all the keys in the dictionary
                if msg.content.lower().rfind(key) != -1:  # If the key is found
                    return response_dict.get(key)  # Return the value of the key
            return ''  # Else return and empty string

        def check_dev(uid):
            """Checks whether the passed ID matches"""
            return uid == 167419045128175616 or uid == 167419045128175616

        try:
            # if message.embeds:  # If the message sent was an embed
            #     if message.author.name == "GitHub":  # If the author is the github bot
            #         embeds = message.embeds[0].to_dict()  # Look to see if the branch is the master branch then pull the new update
            #         if embeds['title'].lower().rfind('elimerebot:master') != -1:
            #             message.content = '$eli PullUpdate'
            #             await self.process_commands(message)
            #             return

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
                response = await check_response_string(botoptions.eli_main_responses, message)  # Check to see if it's a keyword
                god_response = await check_response_string(botoptions.god_responses, message)  # Checks if a keyword from the gods
                if god_response != '':
                    if check_dev(message.author.id):
                        # If either author is the devs
                        message.content = god_response  # Send a god response
                        await message.channel.send(message.content)
                elif response != '':  # Else, send a normal response
                    message.content = response
                    await message.channel.send(message.content)
                elif await check_for_string(message) is True:  # If it's not a keyword, run the BotRespond command
                    message.content = "$eli BotRespond"
                    await self.process_commands(message)
        except AttributeError as e:
            await self.get_guild(config.devServerID).get_channel(config.errorChanID).send(e.__str__() + " in server " + str(message.guild))
            return

    def run(self):
        super().run(config.token)

    async def on_error(self, event, *args, **kwargs):
        """Default error handler"""
        logger = logging.getLogger("discordBot.Logging")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("info.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.error("-------------------------")
        logger.error(f"EVENT: {event}")
        logger.error(traceback.format_exc(limit=-1, chain=False))
        logger.error(f"ARGS: {args}")
        logger.error(f"KWARGS: {kwargs}")


RunBot()

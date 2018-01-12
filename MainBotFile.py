
import modules.functions as funcs
import config, discord, discord.ext.commands.errors, asyncio, botoptions
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
        self.bg_task = self.loop.create_task(self.BackgroundLogCheck())  # This executes the LogCheck function

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

    async def BackgroundLogCheck(self):
        """This checks the Warcraft Logs site and posts a new log if there is one, runs every 10 minutes"""
        await self.wait_until_ready()  # Wait until the bot is finished initializing
        channel = self.get_guild(config.guildServerID).get_channel(config.guildLogChanID)  # Set the channel to send to
        while not self.is_closed():  # As long as the bot is active
            msg = await funcs.CheckForLogs()  # Run the function and store the return
            if msg != "":  # As long as the return isn't an empty string
                await channel.send("Look what I found guys!")  # Post this and the log
                await channel.send(msg)
            else:
                channel = self.get_guild(356544379885846549).get_channel(356545378839035915)
                await channel.send("This isn't an error, just reporting that there are no new logs.")
            await asyncio.sleep(600)

    async def on_member_join(self, member):  # This is fired every time a user joins a server with this bot on it
        channel = discord.utils.get(member.guild.text_channels)  # Select the top most text channel in the server
        # Send this message
        await channel.send("Hello "+member.mention+"! Hope you enjoy your stay here! We're all happy you decided to join us!")

    async def on_message(self, message):
        if message.author.bot is False:  # So the bot won't process it's own messages
            if message.content[0] == '$':  # If the message is actually a command, process it
                await self.process_commands(message)  # This part processes the actual command
                return  # Return so it doesn't run any other part of this
            response = await funcs.CheckResponseString(botoptions.eli_main_responses, message)  # Check to see if it's a keyword
            god_response = await funcs.CheckResponseString(botoptions.god_responses, message) # Checks if a keyword from the gods
            if response or god_response != '':  # If either response isn't an empty string
                if message.author == 167419045128175616 or 198574477347520513:  # If either author is the devs
                    message.content = god_response  # Send a god response
                    await message.channel.send(message.content)
                else:  # Else, send a normal response
                    message.content = response
                    await message.channel.send(message.content)
            elif await funcs.CheckForString(message):  # If it's not a keyword, run the BotRespond command
                message.content = "$eli BotRespond"
                await self.process_commands(message)

    def run(self):
        super().run(config.token)


RunBot()

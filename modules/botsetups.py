from discord.ext import commands
import asyncio
from modules.models.models import Discord, Guild


class BotSetups:

    def __init__(self, bot):
        self.bot = bot

    # noinspection PyPep8Naming
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def SetupDiscord(self, ctx):
        server_id = str(ctx.guild.id)
        discord_dict = {"server_id": server_id, "welcome_channel_id": None, "roles_channel_id": None, "roles_report_channel_id": None,
                        "logs_report_channel_id": None, "mythic_plus_report_channel": None, "wowhead_channel_id": None,
                        "roles_assign": None, "guild": None}

        def check(message):
            return message.author == ctx.author and str(message.channel) == f"Direct Message with {ctx.author}"

        def process_response(message, field):
            if message == "skip":
                return
            else:
                if field == "roles_assign":
                    message = message.split(',')
                    discord_dict[field] = message
                else:
                    discord_dict[field] = message

        try:
            await ctx.author.send("To set up the bot, you're gonna need to enable developer mode on discord!\n"
                                  "To learn how to do that, go to the website {Link Here} and follow the step by step guide.")
            await ctx.author.send("We'll now go step by step to setup the bot! If there is any option you don't want to\n"
                                  "enable just type 'skip' to skip that step!")
            await ctx.author.send("Please enter the Welcome channel ID. This is the channel where you would welcome new\n"
                                  "users to your discord server.")
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "welcome_channel_id")
            await ctx.author.send("Please enter the Roles channel ID. This is the channel where you would have new guild\n"
                                  "members request discord roles.")
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "roles_channel_id")
            await ctx.author.send("Please enter the Roles admin channel ID. This is where the bot will log all roles "
                                  "requests.\nThis is required if you enabled the Roles channel.")
            # wait for id
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "roles_report_channel_id")
            await ctx.author.send("Please enter all the roles you would like to assign to new members. The roles must\n"
                                  "be entered exactly as they are spelled on Discord. Separate them using a comma.\n"
                                  "Example: Test Role, Another Role, And Another Role")
            # wait for text
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "roles_assign")
            await ctx.author.send("Please enter the Logs channel ID. This is the channel where all your warcraft logs\n"
                                  "will be reported. WarcraftLogs is the only site currently supported.")
            # wait for id
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "logs_report_channel_id")
            await ctx.author.send("Please enter the Mythic Plus channel ID. This is where your mythic plus raiderio scores\n"
                                  "will be reported.")
            # wait for id
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "mythic_plus_report_channel")
            await ctx.author.send("Please enter the Wowhead News channel ID. This is where news articles from Wowhead\n"
                                  "will be posted.")
            # wait for id
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "wowhead_channel_id")
            Discord.create(**discord_dict)
            await ctx.author.send("All done storing the information! You can setup your guild settings now!")
        except asyncio.TimeoutError:  # This fires if the user doesn't respond in 20 seconds
            await ctx.channel.send("Oops! You ran out of time! Call the command again when you're ready!")

    # noinspection PyPep8Naming
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def SetupGuild(self, ctx):
        discord_server = Discord.select().where(Discord.server_id == str(ctx.guild.id))
        if len(discord_server) == 0:
            await ctx.channel.send("You have not setup your discord settings. Please do that first then come back to this command.")
            return
        guild_dict = {"name": "", "display_name": "", "server": "", "region": ""}

        def check(message):
            return message.author == ctx.author and str(message.channel) == f"Direct Message with {ctx.author}"

        def process_response(message, field):
            if field == "name":
                guild_dict['name'] = message.lower()
                guild_dict['display_name'] = message
            else:
                guild_dict[field] = message

        try:
            await ctx.author.send("To setup the guild settings you need 3 things.\n"
                                  "Your guild's name, your guild's server, and your guild's region. Be sure to have this "
                                  "information before starting this process.")
            await ctx.author.send("Please enter your guild's name.")
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "name")
            await ctx.author.send("Please enter your guild's server.")
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "server")
            await ctx.author.send("Please enter your guild's region.")
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            process_response(response.content, "region")
            discord_server[0].guild = Guild.create(**guild_dict)
            discord_server[0].save()
            await ctx.author.send("All information stored! Your guild is now linked to your discord server!")
        except asyncio.TimeoutError:  # This fires if the user doesn't respond in 20 seconds
            await ctx.channel.send("Oops! You ran out of time! Call the command again when you're ready!")

def setup(bot):
    bot.add_cog(BotSetups(bot))

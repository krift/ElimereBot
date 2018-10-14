import botoptions
import asyncio
import discord
import os
import random
import config
import aiohttp
from discord.ext import commands


class Commands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['raidtime'])
    async def RaidTime(self, ctx):
        """-Tells the user for the 100th time when raids are."""
        e = discord.Embed(title='Raid Times', colour=discord.Colour.purple())
        e.description = 'Raids are on the following days. Please stop asking me this, you should remember it by now.'
        e.add_field(name='Thursdays', value='630pm Server\n830pm Eastern')
        e.add_field(name='Sundays', value='530pm Server\n730pm Eastern')
        await ctx.channel.send(embed=e)

    @commands.command(aliases=['hello'])
    async def Hello(self, ctx):
        """-Uhhhhh....hellooooo"""
        await ctx.channel.send("I swear to god, I don't know why I even bother, no one listens anyways.")

    @commands.command(aliases=['twitch'])
    async def Twitch(self, ctx):
        """-Holy crap are you even paying attention when I talk?"""
        await ctx.channel.send("https://www.twitch.tv/elimere")

    @commands.command(aliases=['topclip'])
    async def TopClip(self, ctx):
        """-It's the top clip from my channel!"""
        await ctx.channel.send("Check out this amazing clip from my channel!")
        await ctx.channel.send(await self.retrieve_twitch_clip('elimere'))

    @commands.command(aliases=['raidmods'])
    async def RaidMods(self, ctx):
        """-These are the mods required for raiding"""
        await ctx.channel.send("Again, here are the mods required for the 100000th time.\n"
                               "You need the Twitch app installed, download this file, then run it.\n"
                               "http://www.mediafire.com/file/gpc0t8yjhi5369f/Booty_Bay_Surf_Club_Raid_Pack.ccip")

    @commands.command(aliases=['voidelfs'])
    async def Voidelfs(self, ctx):
        """-Tell us how you REALLY feel about Void Elves"""
        await ctx.channel.send("Well first, fuck them\n"
                               "Second..I secretly envy their hair")

    @commands.command(aliases=['mechanics'])
    async def Mechanics(self, ctx):
        """-Will you please stop standing in shit??"""
        await ctx.channel.send("Seriously guys? Are we really still fucking this up after this many months?")

    @commands.command(aliases=['haste'])
    async def Haste(self, ctx):
        """-Is it not enough???"""
        await ctx.channel.send("I don't have enough haste!")

    @commands.command(aliases=['thunder'])
    async def Thunder(self, ctx):
        """-Where are you???"""
        await ctx.channel.send("Did you get enough strawberry mountain water??")

    @commands.command(aliases=['silv'])
    async def Silv(self, ctx):
        """-Damn it Silv!"""
        await ctx.channel.send(random.choice(botoptions.silv))

    @commands.command(aliases=['jems'])
    async def Jems(self, ctx):
        """-One of my besties"""
        await ctx.channel.send(random.choice(botoptions.jems))

    @commands.command(aliases=['mass'])
    async def Mass(self, ctx):
        """-Cant stop wont stop"""
        await ctx.channel.send(random.choice(botoptions.mass))

    @commands.command(aliases=['khaid'])
    async def Khaid(self, ctx):
        """-Tell us another dad joke piano man"""
        await ctx.channel.send(random.choice(botoptions.khaid))

    @commands.command(aliases=['heroes'])
    async def Heroes(self, ctx):
        """-My heroes!"""
        fileLoc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        await ctx.channel.send("Thanks to these guys, who are the best guys I know")
        await ctx.channel.send(file=discord.File(fileLoc+'/media/thing1.jpg'))
        await ctx.channel.send(file=discord.File(fileLoc+'/media/thing2.jpg'))

    @commands.command(hidden=True)
    @commands.cooldown(rate=3, per=300.0, type=commands.BucketType.user)
    async def BotRespond(self, ctx):
        """This responds to certain keywords and strings"""
        async def check_response_string(dict, msg):
            """This checks a dictionary of strings and returns appropriately"""
            for response in dict.keys():  # This looks at all the keys in the dictionary
                if msg.content.lower().rfind(response) != -1:  # If the key is found
                    return dict.get(response)  # Return the value of the key
            return ''  # Else return and empty string

        try:
            # Send a snarky response
            await ctx.channel.send(random.choice(botoptions.eli_calls))

            def check(message):  # This check is used to ensure it's the same user and channel who sent the first message
                return message.author == ctx.author and ctx.channel == message.channel

            response = await self.bot.wait_for('message', check=check, timeout=20.0)  # Wait for the response, 20 seconds max
            response.content = await check_response_string(botoptions.eli_responses, response.content)  # Call this function
            if response.content == '':  # If content is an empty string
                msg = random.choice(botoptions.eli_messages)  # Send a random message
                await ctx.channel.send(msg)
            else:
                if response.content[0] == '$':  # If it's a command, process it
                    await self.bot.process_commands(response)
                else:
                    await ctx.channel.send(response.content)  # Else just send what the bot response was
        except asyncio.TimeoutError:  # This fires if the user doesn't respond in 20 seconds
            await ctx.channel.send("I guess you didn't have anything to say anyways....")

    @staticmethod
    async def retrieve_twitch_clip(channel):
        """Retrieves the newest twitch clip from the channel"""
        # Docs located here https://dev.twitch.tv/docs/v5/reference/clips
        twitchURL = 'https://api.twitch.tv/kraken/clips/top'
        headers = {
            'Client-ID': config.twitchBotId,
            'Accept': 'application/vnd.twitchtv.v5+json'
        }
        params = {
            'channel': channel,
            'period': 'all',
            'limit': '1'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(twitchURL, headers=headers, params=params) as resp:
                json_info = await resp.json()
                await asyncio.sleep(0.250)
                session.close()
        return json_info['clips'][0]['url']


def setup(bot):
    bot.add_cog(Commands(bot))

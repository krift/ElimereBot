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

    # noinspection PyPep8Naming
    @commands.command(aliases=['raidtime'])
    async def RaidTime(self, ctx):
        """-Tells the user for the 100th time when raids are."""
        e = discord.Embed(title='Raid Times', colour=discord.Colour.purple())
        e.description = 'Raids are on the following days. Please stop asking me this, you should remember it by now.'
        e.add_field(name='Thursdays', value='630pm Server\n830pm Eastern')
        e.add_field(name='Sundays', value='530pm Server\n730pm Eastern')
        await ctx.channel.send(embed=e)

    # noinspection PyPep8Naming
    @commands.command(aliases=['hello'])
    async def Hello(self, ctx):
        """-Uhhhhh....hellooooo"""
        await ctx.channel.send("I swear to god, I don't know why I even bother, no one listens anyways.")

    # noinspection PyPep8Naming
    @commands.command(aliases=['twitch'])
    async def Twitch(self, ctx):
        """-Holy crap are you even paying attention when I talk?"""
        await ctx.channel.send("https://www.twitch.tv/elimere")

    # noinspection PyPep8Naming
    @commands.command(aliases=['topclip'])
    async def TopClip(self, ctx):
        """-It's the top clip from my channel!"""
        await ctx.channel.send("Check out this amazing clip from my channel!")
        await ctx.channel.send(await self.retrieve_twitch_clip('elimere'))

    # noinspection PyPep8Naming
    @commands.command(aliases=['raidmods'])
    async def RaidMods(self, ctx):
        """-These are the mods required for raiding"""
        await ctx.channel.send("Again, here are the mods required for the 100000th time.\n"
                               "You need the Twitch app installed, download this file, then run it.\n"
                               "http://www.mediafire.com/file/gpc0t8yjhi5369f/Booty_Bay_Surf_Club_Raid_Pack.ccip")

    # noinspection PyPep8Naming
    @commands.command(aliases=['voidelfs'])
    async def Voidelfs(self, ctx):
        """-Tell us how you REALLY feel about Void Elves"""
        await ctx.channel.send("Well first, fuck them\n"
                               "Second..I secretly envy their hair")

    # noinspection PyPep8Naming
    @commands.command(aliases=['mechanics'])
    async def Mechanics(self, ctx):
        """-Will you please stop standing in shit??"""
        await ctx.channel.send("Seriously guys? Are we really still fucking this up after this many months?")

    # noinspection PyPep8Naming
    @commands.command(aliases=['haste'])
    async def Haste(self, ctx):
        """-Is it not enough???"""
        await ctx.channel.send("I don't have enough haste!")

    # noinspection PyPep8Naming
    @commands.command(aliases=['thunder'])
    async def Thunder(self, ctx):
        """-Where are you???"""
        await ctx.channel.send("Did you get enough strawberry mountain water??")

    # noinspection PyPep8Naming
    @commands.command(aliases=['silv'])
    async def Silv(self, ctx):
        """-Damn it Silv!"""
        await ctx.channel.send(random.choice(botoptions.silv))

    # noinspection PyPep8Naming
    @commands.command(aliases=['jems'])
    async def Jems(self, ctx):
        """-One of my besties"""
        await ctx.channel.send(random.choice(botoptions.jems))

    # noinspection PyPep8Naming
    @commands.command(aliases=['mass'])
    async def Mass(self, ctx):
        """-Cant stop wont stop"""
        await ctx.channel.send(random.choice(botoptions.mass))

    # noinspection PyPep8Naming
    @commands.command(aliases=['khaid'])
    async def Khaid(self, ctx):
        """-Tell us another dad joke piano man"""
        await ctx.channel.send(random.choice(botoptions.khaid))

    # noinspection PyPep8Naming,PyPep8Naming
    @commands.command(aliases=['heroes'])
    async def Heroes(self, ctx):
        """-My heroes!"""
        fileLoc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        await ctx.channel.send("Thanks to these guys, who are the best guys I know")
        await ctx.channel.send(file=discord.File(fileLoc+'/media/thing1.jpg'))
        await ctx.channel.send(file=discord.File(fileLoc+'/media/thing2.jpg'))

    # noinspection PyPep8Naming
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
                await session.close()
        return json_info['clips'][0]['url']


def setup(bot):
    bot.add_cog(Commands(bot))

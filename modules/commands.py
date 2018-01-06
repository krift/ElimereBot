#pylint: disable = W, C

import discord
import asyncio
import random, botoptions
from discord.ext import commands

class Commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['raidtime'])
    async def RaidTime(self, ctx):
        """-Tells the user for the 100th time when raids are."""
        await ctx.channel.send("Raids are on the following days:")
        await ctx.channel.send("Thursday: 830pm Eastern")
        await ctx.channel.send("Sunday: 730pm Eastern")
        await ctx.channel.send("Please stop asking me this, you should remember it by now.")

    @commands.command(aliases=['areyoulistening'])
    async def AreYouListening(self, ctx):
        """-Uhhhhh....hellooooo"""
        await ctx.channel.send("I swear to god, I don't know why I even bother, no one listens anyways.")

    @commands.command(aliases=['twitchchannel'])
    async def TwitchChannel(self, ctx):
        """-Holy crap are you even paying attention when I talk?"""
        await ctx.channel.send("https://www.twitch.tv/elimere")

    @commands.command(aliases=['raidmods'])
    async def RaidMods(self, ctx):
        """-These are the mods required for raiding"""
        await ctx.channel.send("Again, here are the mods required for the 100000th time.")
        await ctx.channel.send("http://www.mediafire.com/file/gpc0t8yjhi5369f/Booty_Bay_Surf_Club_Raid_Pack.ccip")
        await ctx.channel.send("You need the Twitch app installed, download this, then run it.")

    @commands.command(aliases=['silv'])
    async def Silv(self, ctx):
        """-Damn it Silv!"""
        msg = random.choice(botoptions.silv)
        await ctx.channel.send(msg)

    @commands.command(aliases=['voidelfs'])
    async def Voidelfs(self, ctx):
        """-Tell us how you REALLY feel about Void Elves"""
        await ctx.channel.send("Well first, fuck them")
        await ctx.channel.send("Second..I secretly envy their hair")




    @commands.command(aliases=['mechanics'])
    async def Mechanics(self, ctx):
        """Will you please stop standing in shit??"""
        await ctx.channel.send("Seriously guys? Are we really still fucking this up after this many months?")

def setup(bot):
    bot.add_cog(Commands(bot))

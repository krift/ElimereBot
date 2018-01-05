#pylint: disable = W, C

import discord
import asyncio
from discord.ext import commands

class Commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['raidtime'])
    async def RaidTime(self, ctx):
        """Tells the user for the 100th time when raids are."""
        await ctx.channel.send("Raids are on the following days:")
        await ctx.channel.send("Thursday: 830pm Eastern")
        await ctx.channel.send("Sunday: 730pm Eastern")
        await ctx.channel.send("Please stop asking me this, you should remember it by now.")

    @commands.command(aliases=['areyoulistening'])
    async def AreYouListening(self, ctx):
        """Uhhhhh....hellooooo"""
        await ctx.channel.send("I swear to god, I don't know why I even bother, no one listens anyways.")

    @commands.commmand(aliases=['twitchchannel'])
    async def TwitchChannel(self, ctx):
        """Holy crap are you even paying attention when I talk?"""
        await ctx.channel.send("https://www.twitch.tv/elimere")

    @commands.command(aliases=['mods'])
    async def Mods(self, ctx):
        """These are the mods required for raiding"""
        await ctx.channel.send("Again, here are the mods required for the 100000th time.")
        await ctx.channel.send("http://www.mediafire.com/file/gpc0t8yjhi5369f/Booty_Bay_Surf_Club_Raid_Pack.ccip")
        await ctx.channel.send("You need the Twitch app installed, download this, then run it.")

    @commands.command(aliases=['Silv'])
    async def Silv(self, ctx):
        """Damn it Silv!"""
        await ctx.channel.send("Silv you can't cloak everything damn it!")

    @commands.command(aliases=['void elfs'])
    async def Silv(self, ctx):
        """DTell us how you REALLY feel about Void Elves"""
        await ctx.channel.send("Well first, fuck them")
        await ctx.channel.send("Second..i secretly love their hair")




def setup(bot):
    bot.add_cog(Commands(bot))
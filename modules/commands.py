#pylint: disable = W, C

import discord
import asyncio
from discord.ext.commands import Bot
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

    @commands.command(aliases = ['areyoulistening'])
    async def AreYouListening(self, ctx):
        """Uhhhhh....hellooooo"""
        await ctx.channel.send("I swear to god, I don't know why I even bother, no one listens anyways.")

def setup(bot):
    bot.add_cog(Commands(bot))
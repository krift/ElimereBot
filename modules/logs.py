import modules.functions as func
import botoptions
import datetime
import discord
import config
from discord.ext import commands


class Logs:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pullnewlog'])
    async def PullNewLog(self, ctx):
        """This will pull the latest log from warcraft logs"""
        log = await func.CheckForLogs()
        e = discord.Embed(title=log['title'], colour=discord.Colour.purple())
        e.add_field(name='Zone', value=botoptions.zones.get(log['zone'], 'Unknown Zone'))
        e.url = "https://www.warcraftlogs.com/reports/"+log['id']
        e.timestamp = datetime.datetime.fromtimestamp(log['start'] / 1e3)
        channel = self.bot.get_guild(config.guildServerID).get_channel(config.guildLogChanID)
        await channel.send(embed=e)

    # TODO
    @commands.command(hidden=True)
    async def ShowLogByDate(self, ctx):
        """Not implemented, will allow user to pull a log by date"""

    # TODO
    @commands.command(hidden=True)
    async def ShowLogByZone(self, ctx):
        """Not implemented, will allow user to pull all logs by zone"""


def setup(bot):
    bot.add_cog(Logs(bot))

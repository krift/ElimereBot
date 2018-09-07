import modules.functions as func
import botoptions
import datetime
import discord
import modules.database as db
import config
from discord.ext import commands


class WarcraftLogs:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pullnewlog'])
    async def PullNewLog(self, ctx):
        """This will pull the latest log from warcraft logs if there is one to pull"""
        log = await func.CheckForLogs()
        channel = self.bot.get_guild(config.guildServerID).get_channel(config.guildLogChanID)
        if log is None:
            await channel.send("No new logs available.")
        else:
            e = discord.Embed(title=log['title'], colour=discord.Colour.purple())
            e.add_field(name='Zone', value=botoptions.zones.get(log['zone'], 'Unknown Zone'))
            e.url = "https://www.warcraftlogs.com/reports/"+log['id']
            e.timestamp = datetime.datetime.fromtimestamp(log['start'] / 1e3)
            e.set_thumbnail(url="https://www.method.gg/images/world-firsts/raids/bfa/bfa-uldir.jpg")
            e.set_image(url="https://s3.amazonaws.com/file3.guildlaunch.net/462275/tabard.png")
            await channel.send(embed=e)

    @commands.command(aliases=['logbydate, showlogbydate'])
    async def ShowLogByDate(self, ctx, date):
        """Enter the date like such:
        YYYY-MM-DD - 2018-01-05"""
        database = db.Database()
        logs = await database.pull_log_by_date(date)
        if logs is None:
            await ctx.channel.send("There don't appear to be any logs on that date.")
        else:
            msg = ''
            for log in logs:
                msg += '['+log[1]+']https://www.warcraftlogs.com/reports/'+log[0]+' \n'
            await ctx.channel.send("Here are the logs I found!")
            await ctx.channel.send("```"+msg+"```")

    # TODO
    @commands.command(hidden=True)
    async def ShowLogByZone(self, ctx):
        """Not implemented, will allow user to pull all logs by zone"""


def setup(bot):
    bot.add_cog(WarcraftLogs(bot))

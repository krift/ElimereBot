import aiohttp
import asyncio
import botoptions
import datetime
import discord
import config
from discord.ext import commands


class WarcraftLogs:
    def __init__(self, bot):
        self.bot = bot

    async def ensure_table_data_exists(self):
        """Checks to see if the table has any logs in it, if not, pull all logs off the website."""
        if self.bot.database.conn_pool is None:
            channel = self.bot.get_guild(config.devServerID).get_channel(config.reportChanID)
            await channel.send("No active connections to the database.")
            return
        if self.bot.database.check_table('logs') is None:
            a = await self.check_for_logs()

    async def check_for_logs(self):
        """This checks the WarcraftLogs site for new logs"""
        if self.bot.database.conn_pool is None:
            channel = self.bot.get_guild(config.devServerID).get_channel(config.reportChanID)
            await channel.send("No active connections to the database.")
            return
        params = {'api_key': config.warcraftLogsAPI}  # Needed to access the WarcraftLogs api
        url = "https://www.warcraftlogs.com:443/v1/reports/guild/booty%20bay%20surf%20club/maiev/us?"  # This is the URL to pull logs
        async with aiohttp.ClientSession() as session:  # Start a new session
            async with session.get(url, params=params) as resp:  # Get the response
                log_info = await resp.json()  # Store json information
                await asyncio.sleep(0.250)  # Wait to close
                await session.close()  # Close
        logs = []
        for x in log_info:
            log = x
            date = datetime.datetime.fromtimestamp(log['start'] / 1e3)
            date = datetime.datetime.strftime(date, '%Y-%m-%d')
            log_exists = await self.bot.database.read_log_table(str(log['id']))
            if log_exists:
                continue
            else:
                await self.bot.database.insert_log_data(log['id'], date, log['title'], log['zone'])
                logs.append(log)
        return logs

    async def auto_pull_log(self):
        """This is the same as the below command but is used for the task the checks every hour."""
        logs = await self.check_for_logs()
        channel = self.bot.get_guild(config.guildServerID).get_channel(config.guildLogChanID)
        if not logs:
            return
        else:
            for x in logs:
                e = discord.Embed(title=x['title'], colour=discord.Colour.purple())
                e.add_field(name='Zone', value=botoptions.zones.get(x['zone'], 'Unknown Zone'))
                e.url = "https://www.warcraftlogs.com/reports/" + x['id']
                e.timestamp = datetime.datetime.fromtimestamp(x['start'] / 1e3)
                e.set_thumbnail(url=botoptions.zone_pictures.get(x['zone']))
                e.set_image(url="https://s3.amazonaws.com/file3.guildlaunch.net/462275/tabard.png")
                await channel.send(embed=e)

    @commands.command(aliases=['pullnewlog'])
    async def PullNewLog(self, ctx):
        """This will pull the latest log from warcraft logs if there is one to pull"""
        logs = await self.check_for_logs()
        channel = self.bot.get_guild(config.guildServerID).get_channel(config.guildLogChanID)
        async with ctx.channel.typing():
            if not logs:
                await channel.send("No new logs available.")
            else:
                for x in logs:
                    e = discord.Embed(title=x['title'], colour=discord.Colour.purple())
                    e.add_field(name='Zone', value=botoptions.zones.get(x['zone'], 'Unknown Zone'))
                    e.url = "https://www.warcraftlogs.com/reports/"+x['id']
                    e.timestamp = datetime.datetime.fromtimestamp(x['start'] / 1e3)
                    e.set_thumbnail(url=botoptions.zone_pictures.get(x['zone']))
                    e.set_image(url="https://s3.amazonaws.com/file3.guildlaunch.net/462275/tabard.png")
                    await channel.send(embed=e)

    @commands.command(aliases=['logbydate', 'showlogbydate'])
    async def ShowLogByDate(self, ctx, date):
        """Enter the date like such:
        YYYY-MM-DD - 2018-01-05"""
        logs = await self.bot.database.select_log_by_date(date)
        if logs is None:
            await ctx.channel.send("There don't appear to be any logs on that date.")
        else:
            msg = ''
            for log in logs:
                msg += f'[{log[1]}]https://www.warcraftlogs.com/reports/{log[0]} \n'
            await ctx.channel.send("Here are the logs I found!")
            await ctx.channel.send("```"+msg+"```")

    @commands.command(aliases=['logbyzone', 'showlogbyzone'])
    async def ShowLogByZone(self, ctx, *, zone):
        """Enter a raid zone to pull all logs from that zone.
        Uldir
        Antorus, The Burning Throne
        Tomb of Sargeras
        Trial of Valor
        The Nighthold
        Emerald Nightmare
        Hellfire Citadel
        Blackrock Foundry
        Highmaul"""
        # We need to get the zone key based on the value
        raid_zone = 0
        for key, value in botoptions.zones.items():
            if value == zone:
                raid_zone = key
        if raid_zone == 0:
            await ctx.channel.send("You appear to have entered an invalid zone. Check the help command and try again.")
        else:
            logs = await self.bot.database.select_log_by_zone(raid_zone)
            if logs is None:
                await ctx.channel.send("There don't appear to be any logs for that zone.")
            else:
                msg = ''
                await ctx.channel.send("Here are the logs I found!")
                for log in logs:
                    msg += f'[{log[2]}][{log[1]}]https://www.warcraftlogs.com/reports/{log[0]} \n'
                    if len(msg) > 1900:  # This is done incase the amount of logs will not fit into one message
                        await ctx.channel.send("```" + msg + "```")
                        msg = ''
                await ctx.channel.send("```" + msg + "```")


def setup(bot):
    bot.add_cog(WarcraftLogs(bot))

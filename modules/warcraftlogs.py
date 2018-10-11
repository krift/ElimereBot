import aiohttp
import asyncio
import botoptions
import datetime
import discord
import modules.database as db
import config
from discord.ext import commands


class WarcraftLogs:
    def __init__(self, bot):
        self.bot = bot
        self.database = db.Database()
        self.database.create_table(db_string='''CREATE TABLE IF NOT EXISTS logs (id TEXT PRIMARY KEY unique, date TEXT, title TEXT, zone TEXT)''')

    async def check_for_logs(self):
        """This checks the WarcraftLogs site for new logs"""
        async def insert_log_data(*data):
            await self.database.insert_data('''INSERT INTO logs (id, date, title, zone) VALUES(?,?,?,?)''', data)

        async def check_log_by_id(log_id):
            await self.database.read_table('''SELECT id FROM logs where id = ?''', str(log_id))

        params = {'api_key': config.warcraftLogsAPI}  # Needed to access the WarcraftLogs api
        url = "https://www.warcraftlogs.com:443/v1/reports/guild/booty%20bay%20surf%20club/maiev/us?"  # This is the URL to pull logs
        async with aiohttp.ClientSession() as session:  # Start a new session
            async with session.get(url, params=params) as resp:  # Get the response
                log_info = await resp.json()  # Store json information
                await asyncio.sleep(0.250)  # Wait to close
                session.close()  # Close
        logs = []
        for x in log_info:
            log = x
            date = datetime.datetime.fromtimestamp(log['start'] / 1e3)
            date = datetime.datetime.strftime(date, '%Y-%m-%d')
            log_exists = await check_log_by_id(log['id'])
            if log_exists:
                continue
            else:
                await insert_log_data(log['id'], date, log['title'], log['zone'])
                logs.append(log)
        await self.database.close()
        return logs

    @commands.command(aliases=['pullnewlog'])
    async def PullNewLog(self, ctx):
        """This will pull the latest log from warcraft logs if there is one to pull"""
        logs = await self.check_for_logs()
        channel = self.bot.get_guild(config.devServerID).get_channel(config.reportChanID)
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

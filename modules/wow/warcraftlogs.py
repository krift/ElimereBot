import aiohttp
import asyncio
import botoptions
import datetime
import discord
import config
from discord.ext import commands
from modules.models.models import Logs, Guild, Discord


class WarcraftLogs:
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def check_for_logs(server_id):
        """This checks the WarcraftLogs site for new logs"""
        logs = []
        server = Discord.select().where(Discord.server_id == server_id)
        if server[0].guild is None:
            return "There is no guild associated with this discord server."
        params = {'api_key': config.warcraftLogsAPI}  # Needed to access the WarcraftLogs api
        url = f"https://www.warcraftlogs.com:443/v1/reports/guild/{server[0].guild.name}/{server[0].guild.server}/{server[0].guild.region}?"  # This is the URL to pull logs
        async with aiohttp.ClientSession() as session:  # Start a new session
            async with session.get(url, params=params) as resp:  # Get the response
                log_info = await resp.json()  # Store json information
                await asyncio.sleep(0.250)  # Wait to close
                await session.close()  # Close
        if type(log_info) is dict:
            if log_info['status'] == 400:
                return log_info['error']
        for log in log_info:
            date = datetime.datetime.fromtimestamp(log['start'] / 1e3)
            date = datetime.datetime.strftime(date, '%Y-%m-%d')
            log_exists = Logs.get_or_create(log_id=log['id'], log_date=date, log_title=log['title'],
                                            log_zone=log['zone'], guild=Guild.get(Guild.name == server[0].guild.name))
            if log_exists[1] is False:
                continue
            else:
                logs.append(log)
        if len(logs) == 0:
            return "No new logs available"
        if len(logs) > 5:
            return logs.clear()
        return logs

    async def auto_pull_log(self, server_id):
        """This is the same as the above command but is used for the task that checks every 5 minutes."""
        discord_server = Discord.select().where(Discord.server_id == server_id)
        if len(discord_server) == 0:
            return
        if discord_server[0].guild is None:
            return
        if discord_server[0].logs_report_channel_id is None:
            return
        logs = await self.__class__.check_for_logs(server_id)
        channel = self.bot.get_guild(int(server_id)).get_channel(int(discord_server[0].logs_report_channel_id))
        if not logs:
            return
        elif type(logs) == str:
            return
        else:
            for x in logs:
                e = discord.Embed(title=x['title'], colour=discord.Colour.purple())
                e.add_field(name='Zone', value=botoptions.zones.get(x['zone'], 'Unknown Zone'))
                e.url = "https://www.warcraftlogs.com/reports/" + x['id']
                e.timestamp = datetime.datetime.fromtimestamp(x['start'] / 1e3)
                e.set_thumbnail(url=botoptions.zone_pictures.get(x['zone'],
                                                                 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Icon-round-Question_mark.svg/1024px-Icon-round-Question_mark.svg.png'))
                e.set_image(url="https://s3.amazonaws.com/file3.guildlaunch.net/462275/tabard.png")
                await channel.send(embed=e)

    # noinspection PyPep8Naming
    @commands.command(aliases=['pullnewlog'])
    async def PullNewLog(self, ctx):
        """This will pull the latest log from warcraft logs if there is one to pull"""
        discord_server = Discord.select().where(Discord.server_id == str(ctx.guild.id))
        if len(discord_server) == 0:
            await ctx.channel.send("You have not run the setup commands for this server. Please do that first.")
            return
        logs = await self.__class__.check_for_logs(str(ctx.guild.id))
        channel = ctx.guild.get_channel(int(discord_server[0].logs_report_channel_id))
        async with ctx.channel.typing():
            if type(logs) is str:
                await channel.send(logs)
            elif type(logs) is list:
                for x in logs:
                    e = discord.Embed(title=x['title'], colour=discord.Colour.purple())
                    e.add_field(name='Zone', value=botoptions.zones.get(x['zone'], 'Unknown Zone'))
                    e.url = "https://www.warcraftlogs.com/reports/"+x['id']
                    e.timestamp = datetime.datetime.fromtimestamp(x['start'] / 1e3)
                    e.set_thumbnail(url=botoptions.zone_pictures.get(x['zone']))
                    e.set_image(url="https://s3.amazonaws.com/file3.guildlaunch.net/462275/tabard.png")
                    await channel.send(embed=e)

    # noinspection PyPep8Naming
    @commands.command(aliases=['logbydate', 'showlogbydate'])
    async def ShowLogByDate(self, ctx, date):
        """Enter the date like such:
        YYYY-MM-DD - 2018-01-05"""
        logs = Logs.select().where(Logs.log_date == date)
        if logs is None:
            await ctx.channel.send("There don't appear to be any logs on that date.")
        else:
            msg = ''
            for log in logs:
                msg += f'[{log.log_title}]https://www.warcraftlogs.com/reports/{log.log_id} \n'
            await ctx.channel.send("Here are the logs I found!")
            await ctx.channel.send("```"+msg+"```")

    # noinspection PyPep8Naming
    @commands.command(aliases=['logbyzone', 'showlogbyzone'])
    async def ShowLogByZone(self, ctx, *, zone):
        """Enter a raid zone to pull all logs from that zone.
        Battle of Dazar'alor
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
            logs = Logs.select().where(Logs.log_zone == raid_zone)
            if logs is None:
                await ctx.channel.send("There don't appear to be any logs for that zone.")
            else:
                msg = ''
                await ctx.channel.send("Here are the logs I found!")
                for log in logs:
                    msg += f'[{log.log_date}][{log.log_title}]https://www.warcraftlogs.com/reports/{log.log_id} \n'
                    if len(msg) > 1900:  # This is done incase the amount of logs will not fit into one message
                        await ctx.channel.send("```" + msg + "```")
                        msg = ''
                await ctx.channel.send("```" + msg + "```")


def setup(bot):
    bot.add_cog(WarcraftLogs(bot))

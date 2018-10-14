import discord
import config
import datetime
import asyncio
import aiohttp
from discord.ext import commands


async def is_dung_chan(ctx):
    """Used to check if the command was called from the dungeons channel in the guild discord"""
    return ctx.channel.id == config.guildDungChanID


class RaiderIO:

    def __init__(self, bot):
        self.bot = bot

    @commands.check(is_dung_chan)
    @commands.command(aliases=['getstats'])
    async def GetStats(self, ctx, realm, char_name):
        """Pull your raiderio stats from the website
        realm: The realm your character is on
        char_name:"""
        channel = self.bot.get_guild(config.guildServerID).get_channel(config.guildDungChanID)
        async with ctx.channel.typing():
            stats = await self.PullIOStats(realm, char_name)
            # This data is pulled from the http request, see https://raider.io/api#!/character/get_api_v1_characters_profile for more details
            e = discord.Embed(title='RaiderIO Stats', colour=discord.Colour.blue())
            ranks = stats[1]
            scores = stats[2]
            stats = stats[0]
            e.url = stats['profile_url']
            e.set_thumbnail(url=stats['thumbnail_url'])

            e.add_field(name="Character", value='Name: ' + stats['name'] + '\n' +
                        'Race: ' + stats['race'] + '\n' +
                        'Class: ' + stats['class'] + '\n' +
                        'Spec: ' + stats['active_spec_name'] + '\n' +
                        'Faction: ' + stats['faction'])

            e.add_field(name="Score", value="All: " + str(scores['all'])+'\n'+
                        'DPS: '+str(scores['dps'])+'\n'+
                        'Healer: '+str(scores['healer'])+'\n'+
                        'Tank: '+str(scores['tank']))

            e.add_field(name='All Classes and Roles', value='World: ' + str(ranks['overall']['world']) + '\n' +
                        'Region: ' + str(ranks['overall']['region']) + '\n' +
                        'Realm: ' + str(ranks['overall']['realm']))

            if ranks['dps']['world'] > 0:
                e.add_field(name='All DPS', value='World: ' + str(ranks['dps']['world']) + '\n' +
                            'Region: ' + str(ranks['dps']['region']) + '\n' +
                            'Realm: ' + str(ranks['dps']['realm']))

            if ranks['healer']['world'] > 0:
                e.add_field(name='All Healers', value='World: ' + str(ranks['healer']['world']) + '\n' +
                            'Region: ' + str(ranks['healer']['region']) + '\n' +
                            'Realm: ' + str(ranks['healer']['realm']))

            if ranks['tank']['world'] > 0:
                e.add_field(name='All Tanks', value='World: ' + str(ranks['tank']['world']) + '\n' +
                            'Region: ' + str(ranks['tank']['region']) + '\n' +
                            'Realm: ' + str(ranks['tank']['realm']))

            e.add_field(name=stats['class']+' All Roles', value='World: '+str(ranks['class']['world'])+'\n'+
                        'Region: '+str(ranks['class']['region'])+'\n'+
                        'Realm: '+str(ranks['class']['realm']))

            if ranks['class_dps']['world'] > 0:
                e.add_field(name='All '+stats['class']+' DPS', value='World: '+str(ranks['class_dps']['world'])+'\n'+
                            'Region: ' + str(ranks['class_dps']['region']) + '\n' +
                            'Realm: ' + str(ranks['class_dps']['realm']))

            if ranks['class_healer']['world'] > 0:
                e.add_field(name='All '+stats['class']+' Healers', value='World: '+str(ranks['class_healer']['world'])+'\n'+
                            'Region: ' + str(ranks['class_healer']['region']) + '\n' +
                            'Realm: ' + str(ranks['class_healer']['realm']))

            if ranks['class_tank']['world'] > 0:
                e.add_field(name='All '+stats['class']+' Tanks', value='World: '+str(ranks['class_tank']['world'])+'\n'+
                            'Region: ' + str(ranks['class_tank']['region']) + '\n' +
                            'Realm: ' + str(ranks['class_tank']['realm']))

            e.set_footer(text=str(datetime.datetime.now()))

            await channel.send(ctx.message.author.mention)
            await channel.send(embed=e)

    async def PullIOStats(self, realm, char_name):
        """This pulls stats from raiderio"""
        params = {'region': 'us', 'realm': realm, 'name': char_name, 'fields': 'mythic_plus_ranks'}
        url = 'https://raider.io/api/v1/characters/profile?'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                info = await resp.json()
                await asyncio.sleep(0.250)
            params['fields'] = 'mythic_plus_scores'
            async with session.get(url, params=params) as resp:
                score = await resp.json()
                await asyncio.sleep(0.250)
                session.close()
        # Return the base info, the ranks, and the scores into a tuple
        return info, info['mythic_plus_ranks'], score['mythic_plus_scores']


def setup(bot):
    bot.add_cog(RaiderIO(bot))

import discord
import modules.functions as funcs
from discord.ext import commands


class RaiderIO:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['getstats'])
    async def GetStats(self, ctx, realm, char_name):
        """Pull your raiderio stats from the website
        realm:
        char_name:"""
        stats = await funcs.PullIOStats(realm, char_name)
        # This data is pulled from the http request, see https://raider.io/api#!/character/get_api_v1_characters_profile for more details
        e = discord.Embed(title='RaiderIO Stats', colour=discord.Colour.blue())
        e.url = stats['profile_url']
        e.set_thumbnail(url=stats['thumbnail_url'])
        e.add_field(name="Character", value='Name: ' + stats['name'] + '\n' +
                    'Race: ' + stats['race'] + '\n' +
                    'Class: ' + stats['class'] + '\n' +
                    'Spec: ' + stats['active_spec_name'] + '\n' +
                    'Faction: ' + stats['faction'], inline=False)

        e.add_field(name='All Classes and Roles', value='World: ' + str(stats['mythic_plus_ranks']['overall']['world']) + '\n' +
                    'Region: ' + str(stats['mythic_plus_ranks']['overall']['region']) + '\n' +
                    'Realm: ' + str(stats['mythic_plus_ranks']['overall']['realm']))

        if stats['mythic_plus_ranks']['dps']['world'] > 0:
            e.add_field(name='All DPS', value='World: ' + str(stats['mythic_plus_ranks']['dps']['world']) + '\n' +
                        'Region: ' + str(stats['mythic_plus_ranks']['dps']['region']) + '\n' +
                        'Realm: ' + str(stats['mythic_plus_ranks']['dps']['realm']))

        if stats['mythic_plus_ranks']['healer']['world'] > 0:
            e.add_field(name='All Healers', value='World: ' + str(stats['mythic_plus_ranks']['healer']['world']) + '\n' +
                        'Region: ' + str(stats['mythic_plus_ranks']['healer']['region']) + '\n' +
                        'Realm: ' + str(stats['mythic_plus_ranks']['healer']['realm']))

        if stats['mythic_plus_ranks']['tank']['world'] > 0:
            e.add_field(name='All Tanks', value='World: ' + str(stats['mythic_plus_ranks']['tank']['world']) + '\n' +
                        'Region: ' + str(stats['mythic_plus_ranks']['tank']['region']) + '\n' +
                        'Realm: ' + str(stats['mythic_plus_ranks']['tank']['realm']))

        e.add_field(name=stats['class']+' All Roles', value='World: '+str(stats['mythic_plus_ranks']['class']['world'])+'\n'+
                    'Region: '+str(stats['mythic_plus_ranks']['class']['region'])+'\n'+
                    'Realm: '+str(stats['mythic_plus_ranks']['class']['realm']))

        if stats['mythic_plus_ranks']['class_dps']['world'] > 0:
            e.add_field(name='All '+stats['class']+' DPS', value='World: '+str(stats['mythic_plus_ranks']['class_dps']['world'])+'\n'+
                        'Region: ' + str(stats['mythic_plus_ranks']['class_dps']['region']) + '\n' +
                        'Realm: ' + str(stats['mythic_plus_ranks']['class_dps']['realm']))

        if stats['mythic_plus_ranks']['class_healer']['world'] > 0:
            e.add_field(name='All '+stats['class']+' Healers', value='World: '+str(stats['mythic_plus_ranks']['class_healer']['world'])+'\n'+
                        'Region: ' + str(stats['mythic_plus_ranks']['class_healer']['region']) + '\n' +
                        'Realm: ' + str(stats['mythic_plus_ranks']['class_healer']['realm']))

        if stats['mythic_plus_ranks']['class_tank']['world'] > 0:
            e.add_field(name='All '+stats['class']+' Tanks', value='World: '+str(stats['mythic_plus_ranks']['class_tank']['world'])+'\n'+
                        'Region: ' + str(stats['mythic_plus_ranks']['class_tank']['region']) + '\n' +
                        'Realm: ' + str(stats['mythic_plus_ranks']['class_tank']['realm']))
        await ctx.channel.send(embed=e)


def setup(bot):
    bot.add_cog(RaiderIO(bot))

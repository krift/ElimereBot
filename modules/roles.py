from discord.ext import commands
import asyncio, aiohttp, logging, logging.config, config
from modules.models.models import Discord


async def is_roles_channel(ctx):
    server_info = Discord.select().where(Discord.server_id == str(ctx.guild.id))
    if len(server_info) == 0:
        return False
    return str(ctx.channel.id) == Discord.select().where(Discord.server_id == str(ctx.guild.id))[0].roles_channel_id


class Roles:

    def __init__(self, bot):
        self.bot = bot

    # noinspection PyPep8Naming
    @commands.check(is_roles_channel)
    @commands.command(aliases=['requestrole'])
    async def RequestRole(self, ctx):
        """This command is used to request a discord role on the server
        The bot will prompt you for your character name and the realm you're character is on.
        They must be typed in that order with a space in between and spelled correctly.
        example: ExampleCharacter maiev
        """
        server_info = Discord.select().where(Discord.server_id == str(ctx.guild.id))
        guild_info = server_info[0].guild
        await ctx.channel.send("Whoa! Looks like you're requesting a role on discord!")
        await ctx.channel.send("Put your character name and realm(In that order, separated by a space) exactly as "
                               "they are spelled and I'll double check my records!")

        def check(message):  # This check is used to ensure it's the same user and channel who sent the first message
            return message.author == ctx.author and ctx.channel == message.channel
        try:
            response = await self.bot.wait_for('message', check=check,
                                               timeout=20.0)  # Wait for the response, 20 seconds max
            character = response.content.split()
            if len(character) < 2:
                await ctx.channel.send("Oops! You didn't enter the information correctly!")
                return
            response = await Roles.check_character(character[0], character[1])
            if response.get('status') is not None:
                if response['reason'] == 'Realm not found.':
                    await ctx.channel.send("Looks like you entered the realm name incorrectly! Double "
                                           "check and try again!")
                elif response['reason'] == 'Character not found.':
                    await ctx.channel.send("Unfortunately I couldn't find a character with that name! Double check "
                                           "you spelled it correctly and try again!")
            elif response.get('guild') is None:
                await ctx.channel.send("Looks like you aren't in the guild yet or your character hasn't updated."
                                       "Try logging completely out of the game and trying again!")
            elif guild_info.display_name in response['guild']['name']:
                await ctx.channel.send("Assigning roles!")
                roles = ctx.guild.roles
                server_roles = server_info[0].roles_assign
                roles_to_add = []
                for role in roles:
                    if role.name in server_roles:
                        roles_to_add.append(role)
                for role in roles_to_add:
                    await ctx.author.add_roles(role, reason="Bot added requested roles.", atomic=True)
                await self.bot.get_guild(ctx.guild.id).get_channel(int(server_info[0].roles_report_channel_id)).send(
                    f"{ctx.author.name} requested and was granted these roles {server_roles}")

            elif response['guild']['name'] != guild_info.display_name:
                await ctx.channel.send("Looks like you aren't in the guild yet or your character hasn't updated."
                                       "Try logging completely out of the game and trying again!")

            # Run a check to see what guild the character is in here.
        except asyncio.TimeoutError:  # This fires if the user doesn't respond in 20 seconds
            await ctx.channel.send("Oops! You ran out of time! Call the command again when you're ready!")

    @staticmethod
    async def get_token():
        oauth_url = "https://us.battle.net/oauth/token?"
        oauth_params = {'client_id': config.wow_id, 'client_secret': config.wow_secret,
                        'grant_type': 'client_credentials'}
        async with aiohttp.ClientSession() as session:  # Start a new session
            async with session.get(oauth_url, params=oauth_params) as resp:  # Get the response
                token_info = await resp.json()  # Store json information
                await asyncio.sleep(0.250)  # Wait to close
                await session.close()  # Close
        return token_info['access_token']

    @staticmethod
    async def check_character(character, realm):
        token = await Roles.get_token()
        request_url = f'https://us.api.blizzard.com/wow/character/{realm}/{character}?fields=guild&locale=en_US&access_token={token}'
        request_params = {'access_token': token, 'locale': 'en_US'}
        request_info = {}
        try:
            async with aiohttp.ClientSession() as session:  # Start a new session
                async with session.get(request_url, params=request_params) as resp:  # Get the response
                    request_info = await resp.json()  # Store json information
                    await asyncio.sleep(0.250)  # Wait to close
                    await session.close()  # Close
        except aiohttp.client_exceptions.ContentTypeError as e:
            logger = logging.getLogger("discordBot.Logging")
            logger.setLevel(logging.INFO)
            fh = logging.FileHandler("info.log")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.error("-------------------------")
            logger.error(f"{e}")
        return request_info




def setup(bot):
    bot.add_cog(Roles(bot))

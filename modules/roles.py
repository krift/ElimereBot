from discord.ext import commands
import asyncio, aiohttp, config, logging, logging.config


class Roles:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['requestrole'])
    async def RequestRole(self, ctx):
        """This command is used to request a discord role on the server
        The bot will prompt you for your character name and the realm you're character is on.
        They must be typed in that order with a space in between and spelled correctly.
        example: ExampleCharacter maiev
        """
        guild_info = await self.bot.database.select_discordroles_data(str(ctx.guild.id), 'General')
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
            response = await self.check_character(character[0], character[1])
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
            elif response['guild']['name'] == guild_info[2]:  # Make this a database check probably
                await ctx.channel.send("Assigning roles!")
                roles = ctx.guild.roles
                server_roles = guild_info[4]
                roles_to_add = []
                for role in roles:
                    if role.name in server_roles:
                        roles_to_add.append(role)
                for role in roles_to_add:
                    await ctx.author.add_roles(role, reason="Bot added requested roles.", atomic=True)
                await self.bot.get_guild(int(guild_info[1])).get_channel(int(guild_info[5])).send(
                    f"{ctx.author.name} requested and was granted these roles {server_roles}")

            elif response['guild']['name'] != 'Booty Bay Surf Club':
                await ctx.channel.send("Looks like you aren't in the guild yet or your character hasn't updated."
                                       "Try logging completely out of the game and trying again!")

            # Run a check to see what guild the character is in here.
        except asyncio.TimeoutError:  # This fires if the user doesn't respond in 20 seconds
            await ctx.channel.send("Oops! You ran out of time! Call the command again when you're ready!")

    async def check_character(self, character, realm):
        token = await self.get_token()
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

    async def get_token(self):
        oauth_url = "https://us.battle.net/oauth/token?"
        oauth_params = {'client_id': config.wow_id, 'client_secret': config.wow_secret, 'grant_type': 'client_credentials'}
        async with aiohttp.ClientSession() as session:  # Start a new session
            async with session.get(oauth_url, params=oauth_params) as resp:  # Get the response
                token_info = await resp.json()  # Store json information
                await asyncio.sleep(0.250)  # Wait to close
                await session.close()  # Close
        return token_info['access_token']



def setup(bot):
    bot.add_cog(Roles(bot))

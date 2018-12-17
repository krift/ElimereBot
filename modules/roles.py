from discord.ext import commands


class Roles:

    def __init__(self, bot):
        self.bot = bot

    async def request_role(self):
        """Possible command to request a role?"""

    async def approve_role(self):
        """Possible command to approve a requested role?"""


def setup(bot):
    bot.add_cog(Roles(bot))

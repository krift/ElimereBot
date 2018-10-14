from discord.ext import commands


class Tags:

    def __init__(self, bot):
        self.bot = bot
        self.bot.database.create_table('''CREATE TABLE IF NOT EXISTS storage(label TEXT PRIMARY KEY unique, author TEXT, msg TEXT)''')

    @commands.group(aliases=['tags'])
    async def Tags(self, ctx):
        """-Command group for all tags commands"""
        if ctx.invoked_subcommand is None:
            await ctx.channel.send('You need to pass a subcommand. Type $eli help tags for more info.')

    @Tags.command(aliases=['tag', 'set'])
    async def Tag(self, ctx, label: str, *, msg: str):
        """-Stores a message
        $eli tags tag label msg
        label: This must not contain spaces, use _ to represent spaces This_Is_An_Example
        msg: Can be as long as or how ever many lines you want"""
        msg = await self.bot.database.insert_tag_data(label, str(ctx.author), msg)
        await ctx.channel.send(msg)

    @Tags.command(aliases=['update'])
    async def UpdateMessage(self, ctx, label: str, *, msg: str):
        """-Updates the message contained in a specific label"""
        await self.bot.database.update_data(label, msg)
        await ctx.channel.send(label+' updated!')

    @Tags.command(aliases=['retrieve', 'get'])
    async def RetrieveMessage(self, ctx, label):
        """-Retrieves a message
        label: The name of the message to retrieve"""
        msg = await self.bot.database.retrieve_data(label)
        await ctx.channel.send('```'
                               f'Author: {msg[1]}\n'
                               f'{msg[0]}'
                               '```')

    @Tags.command(aliases=['remove', 'delete'])
    async def RemoveMessage(self, ctx, label):
        """-Removes a message
        label: The name of the message to delete"""
        await self.bot.database.delete_data(label)
        await ctx.channel.send('Removed stored message with the label ' + label)

    @Tags.command(aliases=['listall', 'listmessages'])
    async def ListMessages(self, ctx):
        """-Lists all saved messages"""
        msg = await self.bot.database.retrieve_all_labels()
        if msg[1] is True:
            message = "\n".join(str(i) for i in msg[0])
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(msg[0])


def setup(bot):
    bot.add_cog(Tags(bot))

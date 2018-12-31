from discord.ext import commands


class Tags:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['tags'])
    async def Tags(self, ctx):
        """-Command group for all tags commands"""
        if ctx.invoked_subcommand is None:
            await ctx.channel.send('You need to pass a subcommand. Type $eli help tags for more info.')

    @Tags.command(aliases=['tag', 'set'])
    async def Tag(self, ctx, tag: str, *, msg: str):
        """-Stores a message
        $eli tags tag label msg
        tag name: This must not contain spaces, use _ to represent spaces This_Is_An_Example
        msg: Can be as long as or how ever many lines you want"""
        stored = await self.bot.database.insert_tag_data(tag, str(ctx.author), msg)
        if stored is not None:
            await ctx.channel.send("Label stored :D")
        else:
            await ctx.channel.send("The tag could not be stored.")

    @Tags.command(aliases=['update'])
    async def UpdateTag(self, ctx, label: str, *, msg: str):
        """-Updates the message contained in a specific label"""
        updated = await self.bot.database.update_tag_data(label, msg)
        if updated is not None:
            await ctx.channel.send(label+' updated!')
        else:
            await ctx.channel.send("Sorry, I couldn't update the tag :(")

    @Tags.command(aliases=['retrieve', 'get'])
    async def RetrieveTag(self, ctx, label):
        """-Retrieves a message
        label: The name of the message to retrieve"""
        msg = await self.bot.database.select_tag_data(label)
        if msg is None:
            await ctx.channel.send('No tag found.')
        else:
            await ctx.channel.send('```'
                                   f'Author: {msg[1]}\n'
                                   f'{msg[0]}'
                                   '```')

    @Tags.command(aliases=['remove', 'delete'])
    async def RemoveTag(self, ctx, tag):
        """-Removes a message
        label: The name of the message to delete"""
        removed = await self.bot.database.delete_tag_data(tag)
        if removed is not None:
            await ctx.channel.send('Removed stored tag with the tag ' + tag)
        else:
            await ctx.channel.send("Something went wrong :( I wasn't able to remove the tag.")

    @Tags.command(aliases=['listall', 'listmessages'])
    async def ListTags(self, ctx):
        """-Lists all the tags you've created."""
        msg = await self.bot.database.select_all_tag_data(str(ctx.author))
        if msg is not None:
            await ctx.channel.send("Here are all your tags!")
            text = '```'
            for item in msg:
                text += f'{item[0]}: {item[1]}\n'
            text += '```'
            await ctx.channel.send(text)
        else:
            await ctx.channel.send("Looks like there was an issue! I couldn't find any tags!")


def setup(bot):
    bot.add_cog(Tags(bot))

from discord.ext import commands
from modules.models.models import Messages


class Tags:

    def __init__(self, bot):
        self.bot = bot

    # noinspection PyPep8Naming
    @commands.group(aliases=['tags'])
    async def Tags(self, ctx):
        """-Command group for all tags commands"""
        if ctx.invoked_subcommand is None:
            await ctx.channel.send('You need to pass a subcommand. Type $eli help tags for more info.')

    # noinspection PyPep8Naming
    @Tags.command(aliases=['tag', 'set'])
    async def Tag(self, ctx, tag: str, *, msg: str):
        """-Stores a message
        $eli tags tag label msg
        tag name: This must not contain spaces, use _ to represent spaces This_Is_An_Example
        msg: Can be as long as or how ever many lines you want"""
        try:
            Messages.get_or_create(tag_label=tag, tag_author=ctx.author, tag_text=msg)
            await ctx.channel.send("Label stored :D")
        except Exception:
            await ctx.channel.send("The tag could not be stored.")

    # noinspection PyPep8Naming
    @Tags.command(aliases=['update'])
    async def UpdateTag(self, ctx, label: str, *, msg: str):
        """-Updates the message contained in a specific label"""
        try:
            update = Messages.get(Messages.tag_label == label)
            update.tag_text = msg
            update.save()
            await ctx.channel.send("Label updated!")
        except Exception:
            await ctx.channel.send("The tag could not be stored.")

    # noinspection PyPep8Naming
    @Tags.command(aliases=['retrieve', 'get'])
    async def RetrieveTag(self, ctx, label):
        """-Retrieves a message
        label: The name of the message to retrieve"""
        msg = Messages.get(Messages.tag_label == label)
        if msg is None:
            await ctx.channel.send('No tag found.')
        else:
            await ctx.channel.send('```'
                                   f'Author: {msg.tag_author}\n'
                                   f'{msg.tag_text}'
                                   '```')

    # noinspection PyPep8Naming
    @Tags.command(aliases=['remove', 'delete'])
    async def RemoveTag(self, ctx, label):
        """-Removes a message
        label: The name of the message to delete"""
        try:
            q = Messages.delete().where(Messages.tag_label == label)
            q.execute()
            await ctx.channel.send("Label deleted!")
        except Exception as e:
            print(e)
            await ctx.channel.send("The tag could not be deleted.")

    # noinspection PyPep8Naming
    @Tags.command(aliases=['listall', 'listmessages'])
    async def ListTags(self, ctx):
        """-Lists all the tags you've created."""
        msg = Messages.select().where(Messages.tag_author == ctx.author)
        if msg is not None:
            await ctx.channel.send("Here are all your tags!")
            text = '```'
            for item in msg:
                text += f'{item.tag_label}: {item.tag_text}\n'
            text += '```'
            await ctx.channel.send(text)
        else:
            await ctx.channel.send("Looks like there was an issue! I couldn't find any tags!")


def setup(bot):
    bot.add_cog(Tags(bot))

import modules.functions as func
import modules.database as database
import botoptions
import asyncio
import discord
import os
import random
from discord.ext import commands


class Commands:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['storage'])
    async def Storage(self, ctx):
        """-Command group for all storage commands"""
        if ctx.invoked_subcommand is None:
            await ctx.channel.send('You need to pass a subcommand. Type $eli help storage for more info.')

    @Storage.command(aliases=['store', 'set'])
    async def StoreMessage(self, ctx, label: str, *, msg: str):
        """-Stores a message
        $eli storage store label msg
        label: This must not contain spaces, use _ to represent spaces This_Is_An_Example
        msg: Can be as long as or how ever many lines you want"""
        db = database.Database()
        msg = await db.insert_data(label, str(ctx.author), msg)
        await db.close()
        if msg != '':
            await ctx.channel.send(msg)
        else:
            await ctx.channel.send('Stored a message with the label ' + label)

    @Storage.command(aliases=['retrieve', 'get'])
    async def RetrieveMessage(self, ctx, label):
        """-Retrieves a message
        label: The name of the message to retrieve"""
        db = database.Database()
        msg = await db.retrieve_data(label)
        await db.close()
        await ctx.channel.send(msg)

    @Storage.command(aliases=['remove', 'delete'])
    async def RemoveMessage(self, ctx, label):
        """-Removes a message
        label: The name of the message to delete"""
        db = database.Database()
        await db.delete_data(label)
        await db.close()
        await ctx.channel.send('Removed stored message with the label ' + label)

    @Storage.command(aliases=['listall', 'listmessages'])
    async def ListMessages(self, ctx):
        """-Lists all saved messages"""
        db = database.Database()
        msg = await db.retrieve_all_labels()
        await db.close()
        if msg[1] is True:
            message = "\n".join(str(i) for i in msg[0])
            await ctx.channel.send(message)
        else:
            await ctx.channel.send(msg[0])

    @commands.command(aliases=['raidtime'])
    async def RaidTime(self, ctx):
        """-Tells the user for the 100th time when raids are."""
        e = discord.Embed(title='Raid Times', colour=discord.Colour.purple())
        e.description = 'Raids are on the following days. Please stop asking me this, you should remember it by now.'
        e.add_field(name='Thursdays', value='830pm Eastern')
        e.add_field(name='Sundays', value='730pm Eastern')
        await ctx.channel.send(embed=e)

    @commands.command(aliases=['hello'])
    async def Hello(self, ctx):
        """-Uhhhhh....hellooooo"""
        await ctx.channel.send("I swear to god, I don't know why I even bother, no one listens anyways.")

    @commands.command(aliases=['twitch'])
    async def Twitch(self, ctx):
        """-Holy crap are you even paying attention when I talk?"""
        await ctx.channel.send("https://www.twitch.tv/elimere")

    @commands.command(aliases=['topclip'])
    async def TopClip(self, ctx):
        """-It's the top clip from my channel!"""
        await ctx.channel.send("Check out this amazing clip from my channel!")
        await ctx.channel.send(await func.RetrieveTwitchClip('elimere'))

    @commands.command(aliases=['raidmods'])
    async def RaidMods(self, ctx):
        """-These are the mods required for raiding"""
        await ctx.channel.send("Again, here are the mods required for the 100000th time.\n"
                               "You need the Twitch app installed, download this file, then run it.\n"
                               "http://www.mediafire.com/file/gpc0t8yjhi5369f/Booty_Bay_Surf_Club_Raid_Pack.ccip")

    @commands.command(aliases=['voidelfs'])
    async def Voidelfs(self, ctx):
        """-Tell us how you REALLY feel about Void Elves"""
        await ctx.channel.send("Well first, fuck them\n"
                               "Second..I secretly envy their hair")

    @commands.command(aliases=['mechanics'])
    async def Mechanics(self, ctx):
        """-Will you please stop standing in shit??"""
        await ctx.channel.send("Seriously guys? Are we really still fucking this up after this many months?")

    @commands.command(aliases=['haste'])
    async def Haste(self, ctx):
        """-Is it not enough???"""
        await ctx.channel.send("I don't have enough haste!")

    @commands.command(aliases=['thunder'])
    async def Thunder(self, ctx):
        """-Where are you???"""
        await ctx.channel.send("Did you get enough strawberry mountain water??")

    @commands.command(aliases=['silv'])
    async def Silv(self, ctx):
        """-Damn it Silv!"""
        await ctx.channel.send(random.choice(botoptions.silv))

    @commands.command(aliases=['jems'])
    async def Jems(self, ctx):
        """-One of my besties"""
        await ctx.channel.send(random.choice(botoptions.jems))

    @commands.command(aliases=['mass'])
    async def Mass(self, ctx):
        """-Cant stop wont stop"""
        await ctx.channel.send(random.choice(botoptions.mass))

    @commands.command(aliases=['khaid'])
    async def Khaid(self, ctx):
        """-Tell us another dad joke piano man"""
        await ctx.channel.send(random.choice(botoptions.khaid))

    @commands.command(aliases=['heroes'])
    async def Heroes(self, ctx):
        """-My heroes!"""
        fileLoc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        await ctx.channel.send("Thanks to these guys, who are the best guys I know")
        await ctx.channel.send(file=discord.File(fileLoc+'/media/thing1.jpg'))
        await ctx.channel.send(file=discord.File(fileLoc+'/media/thing2.jpg'))

    @commands.command(hidden=True)
    @commands.cooldown(rate=3, per=300.0, type=commands.BucketType.user)
    async def BotRespond(self, ctx):
        """This responds to certain keywords and strings"""
        try:
            if await func.TwitchLive():  # If the function returns true
                await ctx.channel.send("My twitch channel is live! Talk to me there, not here!\n"
                                       "https://www.twitch.tv/elimere\n"
                                       "But I guess I can help you anyways...")
            else:  # Else, send a snarky response
                await ctx.channel.send(random.choice(botoptions.eli_calls))

            def check(message):  # This check is used to ensure it's the same user and channel who sent the first message
                return message.author == ctx.author and ctx.channel == message.channel
            response = await self.bot.wait_for('message', check=check, timeout=20.0)  # Wait for the response, 20 seconds max
            response.content = await func.CheckResponseString(botoptions.eli_responses, response)  # Call this function
            if response.content == '':  # If content is an empty string
                msg = random.choice(botoptions.eli_messages)  # Send a random message
                await ctx.channel.send(msg)
            else:
                if response.content[0] == '$':  # If it's a command, process it
                    await self.bot.process_commands(response)
                else:
                    await ctx.channel.send(response.content)  # Else just send what the bot response was
        except asyncio.TimeoutError:  # This fires if the user doesn't respond in 20 seconds
            await ctx.channel.send("I guess you didn't have anything to say anyways....")


def setup(bot):
    bot.add_cog(Commands(bot))

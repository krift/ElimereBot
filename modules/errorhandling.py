import traceback, discord
from discord.ext import commands


class ErrorHandling:

    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """This event is triggered when an error is raised while invoking a command."""

        try:
            if isinstance(error.original, discord.errors.Forbidden):
                try:
                    await ctx.send("I don't have the required permissions to run this command.")
                except:
                    pass
                finally:
                    return
        except AttributeError:
            pass

        if isinstance(error, commands.MissingPermissions):
            try:
                await ctx.send("You don't have the required permissions for that command.")
            except Exception as e:
                print(e)
            finally:
                return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This bot doesn't accept private messages.")
            except Exception as e:
                print(e)
            finally:
                return

        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                strippedCommand = ctx.message.content.replace(ctx.message.content[0], '')
                strippedCommand = strippedCommand[0:len(strippedCommand)]
                await ctx.send(f"{error}")
                await ctx.send(f"Do $eli help {strippedCommand} to see the correct usage.")
            except Exception as e:
                print(e)
            finally:
                return

        elif isinstance(error, commands.CommandNotFound):
            try:
                await ctx.send(f"There is no command called {ctx.message.content}.")
                await ctx.send("Use $eli help to see a list of available commands.")
            except Exception as e:
                print(e)
                pass
            finally:
                return

        elif isinstance(error, commands.CommandOnCooldown):
            try:
                await ctx.send(error)
            except Exception as e:
                print(e)
                pass
            finally:
                return
        
        elif isinstance(error, commands.errors.BadArgument):
            try:
                await ctx.send("You entered an invalid value. Type $eli help <command> to see the correct usage.")
            except Exception as e:
                print(e)
                pass
            finally:
                return

        elif isinstance(error, commands.CheckFailure):
            return

        var = traceback.format_exception(type(error), error, error.__traceback__)
        e = discord.Embed(title="Command Error", colour=0x32952)
        e.description = f'```py\n{var}\n```'
        e.add_field(name='Command', value=ctx.command)
        e.add_field(name='Server', value=ctx.guild)
        e.add_field(name='Error', value=error)
        await self.bot.get_guild(356544379885846549).get_channel(357317190556581891).send(embed=e)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))

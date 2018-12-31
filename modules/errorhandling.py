import discord
import logging
import logging.config
from discord.ext import commands


class Logging:

    @staticmethod
    def log_command_error(command, server, error):
        logger = logging.getLogger("discordBot.Logging")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler("info.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.error("-------------------------")
        logger.error(f"Command: {command}")
        logger.error(f"Server: {server}")
        logger.error(f"Error: {error}")


class ErrorHandling:
    """
    This class handles all discord command specific errors. At the bottom of the class will be a generic catch all
    logging object for any error that isn't explicitly handled.
    """

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
            except:
                pass
            finally:
                return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This bot doesn't accept private messages.")
            except:
                pass
            finally:
                return

        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                prefix = self.bot.command_prefix
                stripped_command = ctx.message.content.replace(prefix, '')
                stripped_command = stripped_command[0:len(stripped_command)]
                await ctx.send(f"{error}")
                await ctx.send(f"Do {prefix}help {stripped_command} to see the correct usage.")
            except:
                pass
            finally:
                return

        elif isinstance(error, commands.CommandNotFound):
            try:
                prefix = self.bot.command_prefix
                await ctx.send(f"There is no command called {ctx.message.content}.")
                await ctx.send(f"Use {prefix} help to see a list of available commands.")
            except:
                pass
            finally:
                return

        elif isinstance(error, commands.CommandOnCooldown):
            try:
                pass
            except:
                pass
            finally:
                return
        
        elif isinstance(error, commands.errors.BadArgument):
            try:
                prefix = self.bot.command_prefix
                await ctx.send(f"You entered an invalid value. Type {prefix} help {ctx.command} to see the correct usage.")
            except:
                pass
            finally:
                return

        elif isinstance(error, commands.CheckFailure):
            return

        # This should catch all unexpected errors that come from commands and log them.
        logger = Logging()
        logger.log_command_error(ctx.command, ctx.guild, error)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))

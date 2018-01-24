# -*- coding: utf-8 -*-
""" General commands for the Project Manager Bot.

Todo
----
*

"""

from discord.ext import commands  # Used to create commands for the bot to use
import database  # Used to connect to the database
from settings import *  # Imports all of the settings variables

class General:
    """ Commands that are used to interact with server-specific definitions. Useful for storing keyword definitions
    and links

    """

    def __init__(self, bot):
        """ Constructs the General class, adding the commands to the given bot.

        Parameters
        ----------
        bot : discord.ext.commands.Bot
            The bot to have the commands added to.

        """

        # Sets the bot of the class to the given bot
        self.bot = bot

    @commands.command(pass_context=True)
    async def invite(self, ctx):
        """ Sends an invite link to the channel the command was issued in.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.

        """

        # Sends the invite link to the live bot
        await ctx.message.channel.send("Thank-you for your interest in {}! "
                                       "Here is the link for the bot:\n{}".
                                       format(self.bot.user.name, bot_settings['invite']))


def setup(bot):
    """ Used to import the commands for use in the given bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        The bot to have the commands added to.

    """

    # Adds the commands to the bot
    bot.add_cog(General(bot))

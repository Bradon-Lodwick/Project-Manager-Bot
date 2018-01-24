# -*- coding: utf-8 -*-
""" This file contains all of the commands associated with the definition function of the bot.

Todo
----
*

"""

from discord.ext import commands  # Used to create commands for the bot to use
import database  # Used to connect to the database
from settings import *  # Imports all of the settings variables


class Definitions:
    """ Commands that are used to interact with server-specific definitions. Useful for storing keyword definitions
    and links

    """

    def __init__(self, bot):
        """ Constructs the Definitions class, adding the commands to the given bot.

        Parameters
        ----------
        bot : discord.ext.commands.Bot
            The bot to have the commands added to.

        """

        # Sets the bot of the class to the given bot
        self.bot = bot

    @commands.command(pass_context=True)
    async def ins_def(self, ctx, command, definition):
        """ Inserts a definition into the definition database.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.
        command : str
            The command for the definition to be stored.
        definition : str
            The definition to be stored.

        """

        # Gets the guild from the context
        guild = ctx.message.guild
        # Gets the channel from the context
        channel = ctx.message.channel
        # Tries to insert the definition into the database, getting whether or not it was successful in doing so
        success = database.ins_def(db_settings['path'], guild.id, command, definition, commit=True)
        # If insert successful, sends a success message
        if success:
            # Sends a success message
            await channel.send("Definition added!")
        # If unsuccessful, and definition exists, output that the command already exists
        elif not success and database.get_def(db_settings['path'], guild.id, command) is not None:
            await channel.send("Definition already exists, delete the definition first or use a different keyword.")
        # If unsuccessful, and definition doesn't exist, output an error occurred
        else:
            await channel.send("There was an error inserting the definition, please try again.")

    @commands.command(pass_context=True)
    async def get_def(self, ctx, command):
        """ Gets a definition from the definition database.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.
        command : str
            The command for the desired definition.

        """

        # Gets the guild from the context
        guild = ctx.message.guild
        # Gets the channel from the context
        channel = ctx.message.channel
        # Gets the definition from the database
        definition = database.get_def(db_settings['path'], guild.id, command)
        # Checks to see if the definition existed
        if definition is not None:
            # Sends the definition
            await channel.send(definition)
        else:
            # Sends an error message
            await channel.send("That definition doesn't exist in the database.")

    @commands.command(pass_context=True)
    async def del_def(self, ctx, command):
        """ Deletes a definition from the database.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.
        command : str
            The command of the definition to have removed from the database.

        """

        # Gets the guild from the context
        guild = ctx.message.guild
        # Gets the channel from the context
        channel = ctx.message.channel
        # Removes the definition from the database
        database.del_def(db_settings['path'], guild.id, command, commit=True)
        # Sends a success message
        await channel.send("Definition removed from the database!")


def setup(bot):
    """ Used to import the commands for use in the given bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        The bot to have the commands added to.

    """

    # Adds the commands to the bot
    bot.add_cog(Definitions(bot))

# -*- coding: utf-8 -*-
""" This file contains all of the commands associated with the wikipedia function of the bot.

Todo
----
*

"""

from discord.ext import commands  # Used to create commands for the bot to use
import discord  # Used for error handling
import wikipedia  # Wikipedia library

class Wiki:
    """ Commands that are used to search Wikipedia.

    """

    def __init__(self, bot):
         """ Constructs the Wiki class, adding the commands to the given bot.

         Parameters
         ----------
         bot : discord.ext.commands.Bot
             The bot to have the commands added to.

         """

         # Sets the bot of the class to the given bot
         self.bot = bot

    @commands.command(pass_context=True)
    async def wiki(self, ctx, subject):
        """ Searches wikipedia for a brief summary of a given term or concept.

        Format: !wiki search
        Where search is the topic to be searched on wikipedia

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.
        subject : str
            The argument that will be searched in wikipedia

        """

        # The channel the message was sent in
        channel = ctx.message.channel

        search = wikipedia.search(subject)


        i = 0
        while i < 4 and i in range(len(search)):
            try:
                wiki = wikipedia.summary(search[i])
            except wikipedia.DisambiguationError:
                search.remove(search[i])
            else:
                if i == 0:
                    await channel.send("Please Specify an Option:")
                await channel.send(content="{}: {}".format(i+1, search[i]))
                i += 1

        if len(search) != 0:
            def check(m):
                return len(m.content) == 1 and m.content in '1234' and m.channel == channel

            msg = await self.bot.wait_for('message', check=check)

            await channel.send(content=wikipedia.page(search[int(msg.content)-1]).url)
        else:
            await channel.send(content="Sorry I couldn't find anything")

def setup(bot):
    """ Used to import the commands for use in the given bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        The bot to have the commands added to.

    """

    # Adds the commands to the bot
    bot.add_cog(Wiki(bot))
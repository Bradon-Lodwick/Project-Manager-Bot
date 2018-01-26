# -*- coding: utf-8 -*-
""" This file contains all of the commands associated with the groups function of the bot.

Todo
----
*

"""

from discord.ext import commands  # Used to create commands for the bot to use
import discord  # Used for error handling


class Groups:
    """ Commands that are used to create new groups withing the discord server.
    Groups get their own role, and a category of channels locked to their group.

    """

    def __init__(self, bot):
        """ Constructs the Groups class, adding the commands to the given bot.

        Parameters
        ----------
        bot : discord.ext.commands.Bot
            The bot to have the commands added to.

        """

        # Sets the bot of the class to the given bot
        self.bot = bot

    @commands.command(pass_context=True)
    async def create_group(self, ctx, name):
        """ Creates a new group by making a role and role-locked text and voice channels for that group.
        Sends a message saying whether or not the command was successful.

        Format: !create_group group_name
        where group_name is the intended name of group

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.
        name : str
            The desired name for the group. Will be role name and prefix the chats.

        """
        # The guild the message was sent in
        guild = ctx.message.guild
        # The author of the message
        author = ctx.message.author
        # The channel the message was sent in
        channel = ctx.message.channel

        # Checks if the name only has alphabetic
        if name.isalpha():
            # Creates the group role
            group_role = await guild.create_role(name=name, mentionable=True)
            # Adds the bot to the new role
            await ctx.me.add_roles(group_role)
            # Adds the author to the new role
            await author.add_roles(group_role)

            # Setup the permissions to be passed to the channels
            everyone_perm = discord.PermissionOverwrite(read_messages=False)
            group_perm = discord.PermissionOverwrite(read_messages=True)
            permissions = {guild.default_role: everyone_perm, group_role: group_perm}

            # Creates the category channel for the group
            category = await guild.create_category(name, overwrites=permissions)
            # Creates the important text channel for the group
            await guild.create_text_channel("{}-important".format(name), category=category)
            # Creates the general text channel for the group
            await guild.create_text_channel("{}-text".format(name), category=category)
            # Creates the voice channel for the group
            await guild.create_voice_channel("{}-voice".format(name), category=category)

            # Send a success message after completing making the channels and role
            await channel.send(content="The group has been successfully created.")
        else:
            await channel.send(content="Use only letters as the group name.")

    @commands.command(pass_context=True)
    async def add_to_group(self, ctx):
        """ Adds the given group role to the users mentioned. Must already have the role in order to add the users to it.
        Sends a message to the channel that the command was sent through saying whether the command was successful.

        Format: !add_to_group @_group_name_ @user1 @user2 @user3...
        Where group name is the name of the group and users are the intended members

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context of the message.

        """
        # Gets the author of the message
        author = ctx.message.author
        # Gets the channel the message was send in
        channel = ctx.message.channel
        # Checks to see that only 1 role was mentioned
        if len(ctx.message.role_mentions) != 1:
            await channel.send(content="Please mention the group (only 1 group) that you would like to add the users to.")
        # Checks to see if the role mentioned is in the user's role list
        elif ctx.message.role_mentions[0] not in author.roles:
            await channel.send(content="You must belong to the group in order to add users to it.")
        # Checks to see if the user mentioned any users
        elif len(ctx.message.mentions) < 1:
            await channel.send(content="Please mention the users that you would like to have added to the group.")
        # Adds the users to the given role, as all security checks have passed
        else:
            # Try to add the users to the role
            try:
                # Loops through all the users
                for user in ctx.message.mentions:
                    # Checks if the user is already in the role
                    if ctx.message.role_mentions[0] not in user.roles:
                        # Adds the role to the user
                        await user.add_roles(ctx.message.role_mentions[0])
                await channel.send(content="The given users have been successfully added to the given group.")
            # Exceptions in the case of the bot not having permissions
            except discord.Forbidden:
                await channel.send(content="I don't have permissions to give user roles.")


def setup(bot):
    """ Used to import the commands for use in the given bot.

    Parameters
    ----------
    bot : discord.ext.commands.Bot
        The bot to have the commands added to.

    """

    # Adds the commands to the bot
    bot.add_cog(Groups(bot))

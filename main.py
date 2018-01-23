# -*- coding: utf-8 -*-
""" This file contains all of the commands and startup processes to run the project manager bot.

Explanation
-----------
* The bot is created through the commands.Bot function from the discord.py library.
* @bot.event on_ready() is used to print information about the bot on startup.
* @bot.commands is used to create commands for users to use when interacting with the bot.
* bot.run is used to actually start the bot.

Todo
----
*

"""
import discord  # Used for basic discord api functionality
from discord.ext import commands  # Used to create commands for the bot
import ruamel.yaml as yaml  # Used to access yaml settings files
import database  # Used to interact with the database


# Get config settings from the settings.yml file
with open('settings.yml', 'r') as setup_stream:
    # Config variables will be found here
    cfg = yaml.load(setup_stream, Loader=yaml.Loader)


# Setup the commands for the bot
bot = commands.Bot(command_prefix=cfg['bot']['symbol'], description='Project Manager Bot')


# Runs when the bot starts
@bot.event
async def on_ready():
    # Prints out bot information
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_context=True)
async def create_group(ctx, name):
    """ Creates a new group by making a role and role-locked text and voice channels for that group.
    Sends a message saying whether or not the command was successful.

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


@bot.command(pass_context=True)
async def add_to_group(ctx):
    """ Adds the given group role to the users mentioned. Must already have the role in order to add the users to it.
    Sends a message to the channel that the command was sent through saying whether the command was successful.

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
        await channel.send(content="Please mention the role (only 1 role) that you would like to add the users to.")
    # Checks to see if the role mentioned is in the user's role list
    elif ctx.message.role_mentions[0] not in author.roles:
        await channel.send(content="You must belong to the role in order to add users to it.")
    # Checks to see if the user mentioned any users
    elif len(ctx.message.mentions) < 1:
        await channel.send(content="Please mention the users that you would like to have added to the role.")
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
            await channel.send(content="The given users have been successfully added to the given role.")
        # Exceptions in the case of the bot not having permissions
        except discord.Forbidden:
            await channel.send(content="I don't have permissions to give user roles.")


@bot.command(pass_context=True)
async def ins_def(ctx, command, definition):
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
    # Inserts the definition into the database
    database.ins_def(cfg['db']['path'], guild.id, command, definition, commit=True)
    # Sends a success message
    await channel.send("Definition added!")


@bot.command(pass_context=True)
async def get_def(ctx, command):
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
    definition = database.get_def(cfg['db']['path'], guild.id, command)
    # Checks to see if the definition existed
    if definition is not None:
        # Sends the definition
        await channel.send(definition)
    else:
        # Sends an error message
        await channel.send("That definition doesn't exist in the database.")


@bot.command(pass_context=True)
async def del_def(ctx, command):
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
    database.del_def(cfg['db']['path'], guild.id, command, commit=True)
    # Sends a success message
    await channel.send("Definition removed from the database!")


if __name__ == "__main__":
    """ The main function of the bot, which is used to actually start the bot."""
    # Runs the bot
    bot.run(cfg['bot']['token'])

import discord  # Used for basic discord api functionality
from discord.ext import commands  # Used to create commands for the bot
import asyncio  # Used for asynchronous processing
import ruamel.yaml as yaml  # Used to access yaml settings files


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

    :param ctx: The context of the message

    :param name: The desired name for the group. Will be role name and prefix the chats.
    :type name: str
    """
    # The server the message was sent in
    server = ctx.message.server

    # Creates the group role
    group_role = await bot.create_role(server, name=name, mentionable=True)
    # Adds the author to the new role
    await bot.add_roles(ctx.message.author, group_role)

    # Setup the permissions to be passed to the channels
    everyone_perm = discord.PermissionOverwrite(read_messages=False)
    group_perm = discord.PermissionOverwrite(read_messages=True)

    # Creates the important text channel
    await bot.create_channel(
        ctx.message.server, "{}-important".format(name),
        (ctx.message.server.default_role, everyone_perm), (group_role, group_perm), type=discord.ChannelType.text
    )
    # Creates the general text channel
    await bot.create_channel(
        ctx.message.server, "{}-general".format(name),
        (ctx.message.server.default_role, everyone_perm), (group_role, group_perm), type=discord.ChannelType.text
    )
    # Creates the general voice chat
    await bot.create_channel(
        ctx.message.server, "{}-general".format(name),
        (ctx.message.server.default_role, everyone_perm), (group_role, group_perm), type=discord.ChannelType.voice
    )


# Adds a user to a group, if the user running the command is in the group
@ bot.command(pass_context=True)
async def add_to_group(ctx):
    """ Adds the given group role to the users mentioned. Must already have the role in order to add the users to it.

    :param ctx: The context of the message.
    """
    # Gets the author of the message.
    author = ctx.message.author
    # Checks to see that only 1 role was mentioned
    if len(ctx.message.role_mentions) != 1:
        await bot.say("Please mention the role that you would like to add the users to.")
    # Checks to see if the role mentioned is in the user's role list
    elif ctx.message.role_mentions[0] not in author.roles:
        await bot.say("You must belong to the role in order to add users to it.")
    # Checks to see if the user mentioned any users
    elif len(ctx.message.mentions) < 1:
        await bot.say("Please mention the users that you would like to have added to the role.")
    # Adds the users to the given role, as all security checks have passed
    else:
        # Try to add the users to the role
        try:
            # Loops through all the users
            for user in ctx.message.mentions:
                # Checks if the user is already in the role
                if ctx.message.role_mentions[0] not in user.roles:
                    # Adds the role to the user
                    await bot.add_roles(user, ctx.message.role_mentions[0])
            await bot.say("The given users have been successfully added to the given role.")
        # Exceptions in the case of the bot not having permissions
        except discord.Forbidden:
            await bot.say("I don't have permissions to give user roles.")


# Runs the bot
bot.run(cfg['bot']['token'])

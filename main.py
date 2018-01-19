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


# Adds a user to a group, if the user running the command is in the group
@ bot.command(pass_context=True)
async def add_to_group(ctx, role, *users):
    author = ctx.message.author
    # TODO continue here
    if discord.Role(id=role) in author.roles:
        await bot.say("you can add the users to the role")
    else:
        await bot.say("you can not add the users to this role")


@bot.command(pass_context=True)
async def test(ctx, *args):
    await bot.say(ctx.message.author.mention)
    for arg in args:
        await bot.say(arg)


# Runs the bot
bot.run(cfg['bot']['token'])

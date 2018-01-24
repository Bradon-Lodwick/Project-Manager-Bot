# -*- coding: utf-8 -*-
""" This file is used to setup and start the project manager bot. To start the bot, run this file.
You should not add commands into this file, instead add commands into their appropriate category in the commands folder.
If there is no applicable category, make a new category by creating a new category file.

Explanation
-----------
* Sets the bot variable up
* Imports all the commands from the commands folder
* Asks which bot token to use, the dev or live token
* Starts the bot

Todo
----
*

"""

from discord.ext import commands  # Used to create commands for the bot
from settings import *  # Imports all of the settings variables
import glob  # Used to retrieve all of the files in the command directory and load all bot commands


# Setup the bot
bot = commands.Bot(command_prefix=bot_settings['symbol'], description=bot_settings['description'])


@bot.event
async def on_ready():
    """ Prints out information when the bot is started.

    """

    # Prints out bot information
    print('--------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')


if __name__ == "__main__":
    """ The main function of the bot, which is used to actually start the bot. Also adds the extensions from the
    command folder. Allows user to specify which bot token to use, picking between a live and development version.
    
    """

    # Heading sent to output at beginning of the command setup
    print("START COMMAND SETUP\n-------------------")
    # Load all of the command extensions from the commands folder by looping through .py files
    for file in glob.glob("{}*.py".format(bot_settings['c_path'])):
        # Converts the file name to the acceptable string for the load_extension method
        file = file.rstrip('.py')  # Strips the .py extension
        file = file.replace('/', '.')  # Replaces the /'s in the path with .'s
        file = file.replace('\\', '.')  # Replaces the \'s in the path with .'s
        # Tries to load the given extension
        try:
            # Loads the extension
            bot.load_extension(file)
            # Outputs successful loading message
            print("Loaded the {} extension".format(file))
        # Handles errors loading the extension
        except ModuleNotFoundError as e:
            # Outputs error message
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}.\n{}'.format(file, exc))
    # Outputs a message saying command setup phase completed
    print("Command setup phase complete.\n")

    # Heading sent to output to signify the beginning of the specification phase
    print("START SELECT PHASE\n------------------")
    # Gets user input to select which bot token to use
    select = input('Run using the live bot (1) or the dev bot (2) token?\n>')
    # Loops until the input was valid
    while select != '1' and select != '2':
        select = input('Please only use input 1 for the live bot or 2 for the dev bot token.\n>')
    # Sets token to appropriate value based on select variable
    if select == '1':
        token = bot_settings['live_token']
        print("The bot will be started using the live version token.")
    elif select == '2':
        token = bot_settings['dev_token']
        print("The bot will be started using the development version token.\n")

    # Runs the bot
    bot.run(token)

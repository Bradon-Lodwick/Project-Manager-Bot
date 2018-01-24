# -*- coding: utf-8 -*-
""" This file contains all variables that are used as settings, such as file paths and bot token information.
It is used throughout the bot, so be careful changing values here.

Changes Needed
--------------
To run the bot, you will need to change sections with values of 'change-me' to their actual values.  Most notably,
you need to change the token for your live bot and invite link. Make sure the invite link has the following permissions:
* Manage Roles
* Read Messages
* Manage Messages
* Mention Everyone
* Manage Channels
* Send Messages
* Read Message History
If you plan on using the dev bot token, it will also need to be changed.
Finally, changed the name of the file from example_settings.py to settings.py

Todo
----
*

"""

# Variables associated with the discord bot
bot_settings = {
    'live_token': "change-me",  # The live bot token
    # The invite link for the live bot
    'invite':
        "change-me",
    'dev_token': "change-me",  # The dev bot token
    'description': "A bot made to aid in managing multiple projects in a discord server",  # The bot description
    'symbol': "!",  # The command symbol the bot should use
    'c_path': "commands/",  # The path to the folder containing bot command extensions
}

# Variables associated with the database
db_settings = {
    'path': "databases/pm.db",  # The path to the bot's database
}

import discord
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, MissingRequiredArgument, ChannelNotFound, MemberNotFound, BucketType
import random
import asyncio
import tokens

# put the name of all the files you want loaded in
initial_extensions = ["Blackjack"]

client = commands.Bot(command_prefix="=", case_insensitive=True)

# load all the file commands in to this file
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


client.run(tokens.vals)

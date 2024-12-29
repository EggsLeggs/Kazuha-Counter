import datetime

import discord
from discord.ext import commands

import kazuConfig

description = """
An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    users = {}
    print("Preparing to collect history")
    channel=await bot.fetch_channel("858959824719708191")
    time=datetime.datetime(2022,7,16,1,15)
    messages = await channel.history(after=time, limit=99004).flatten()
    print("Retrieved History")
    total = len(messages)
    for olivia in range(len(messages)):
        print(f'Message {olivia}/{total}')
        # msg = await channel.fetch_message(messages[olivia].id)
        # content = msg.content.lower()
        # if 'kazuha slash' not in content:
        #     next
        author = messages[olivia].author.id
        if author in users:
            users[author] += 1
        else:
            users[author] = 1
    sorted_dict = {}
    sorted_keys = sorted(users, key=users.get, reverse=True)
    for cringe in sorted_keys:
        sorted_dict[cringe] = users[cringe]
    first = sorted_keys[0]
    second = sorted_keys[1]
    third = sorted_keys[2]
    print(sorted_dict)
    print('--------')
    print(f'1st: {first} = {sorted_dict[first]}')
    print(f'2nd: {second} = {sorted_dict[second]}')
    print(f'3rd: {third} = {sorted_dict[third]}')



bot.run(kazuConfig.discordKey)

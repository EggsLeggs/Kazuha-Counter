import discord
from discord.ext import commands
from discord.ext.commands import is_owner
from datetime import datetime
import kazuConfig
#----------------------------------------------------------------
description = "Counts Kazuha Slashes"
intents = discord.Intents.default()
activity = discord.Activity(type=discord.ActivityType.watching, name="discord.gg/kazuhamains")
bot = commands.Bot(command_prefix="KC$", activity=activity, description=description, intents=intents)

@bot.event
async def on_ready():
    print('Ready')

@bot.command()
@commands.is_owner()
async def leaderboard(ctx):
    LBcount = {}
    LBtime = {}
    x = 0
    print("history started")
    channel = bot.get_channel(858959824719708191)
    for msg in await channel.history(limit=None).flatten():
        print (x)
        x += 1
        if (msg.author.id in LBtime) and ("kazuhaslash" in ((msg.content).lower()).replace(" ", "")):
            if (LBtime[msg.author.id]-msg.created_at).total_seconds() > 5:
                LBcount[msg.author.id] = LBcount[msg.author.id] + 1
                LBtime[msg.author.id] = msg.created_at
        elif (msg.author.id not in LBtime) and ("kazuhaslash" in ((msg.content).lower()).replace(" ", "")):
            LBcount[msg.author.id] = 1
            LBtime[msg.author.id] = msg.created_at
        else:
            next
    print("history collected")
    LBcounted = sorted(((v,k) for k,v in LBcount.items()))
    first = LBcounted[-1][1]
    second = LBcounted[-2][1]
    third = LBcounted[-3][1]
    print(LBcount)
    print(f"1st - UserID: {first} Messages: {LBcount[first]}")
    print(f"2nd - UserID: {second} Messages: {LBcount[second]}")
    print(f"3rd - UserID: {third} Messages: {LBcount[third]}")
    await ctx.send(f"1st - UserID: {first} Messages: {LBcount[first]}\n2nd - UserID: {second} Messages: {LBcount[second]}\n3rd - UserID: {third} Messages: {LBcount[third]}")
#------------------------------------------------------------------------------#
bot.run(kazuConfig.discordKey)

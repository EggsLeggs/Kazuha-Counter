import os
import pickle
import re
import atexit

import discord
from discord.commands import Option
import kazuConfig


intents = discord.Intents.default()
intents.members = True

intents = discord.Intents.all()
activity = discord.Activity(
    type=discord.ActivityType.playing,
    name="Kazuha Slash"
)
bot = discord.Bot(
    activity=activity,
    intents=intents
)

file_path = '.\kazu_slash.pkl'

num2words = {0: 'Zero', 1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}

if os.path.isfile(file_path):
    with open(file_path, 'rb') as f:
        slash_dic = pickle.load(f)
else: 
    slash_dic = {}

kazuha_slash = bot.create_group("kazuha-slash", "Commands used in the Kazuha Slash Event.", guild_ids=[836722051980066856])

regexPattern = re.compile(r"kazuha( )?slash")

@kazuha_slash.command(name="rank", description="Gets the user's ranking in the Kazuha Slash event.")
async def rank(
    ctx: discord.ApplicationContext,
    user: Option(discord.Member, type=6, name="user", description="Enter a user to lookup", required=False)
):
    if not user:
        user = ctx.user
    if user not in ctx.guild.members:
        return await ctx.respond(embed=errorMessage(
            errorMessage='User Not In Guild'
        ))
    if user.id in slash_dic:
        sorted_keys = sorted(slash_dic, key=slash_dic.get, reverse=True)
        position = ordinaltg(sorted_keys.index(user.id)+1)
        description = f'• Leaderboard Position: {position}\n• Kazuha Slashes: {slash_dic[user.id]}'
    else:
        description = f'{user.mention} is yet to slash, check the pins for the rules!'
    await ctx.respond(embed=titledMessage("Kazuha Slash Rank", description))

@kazuha_slash.command(name="leaderboard", description="Gets the current top rankers")
async def leaderboard(
    ctx: discord.ApplicationContext,
):
    increments = min(5, len(slash_dic))
    description = f'**Top {num2words[increments]}:**'
    sorted_keys = sorted(slash_dic, key=slash_dic.get, reverse=True)
    for i in range(increments):
        slashes = slash_dic[sorted_keys[i]]
        description += f'\n• **{ordinaltg(i + 1)}** · <@{sorted_keys[i]}> · {slashes} {pl(slashes)}'
    if ctx.author.id in slash_dic:
        position = ordinaltg(sorted_keys.index(ctx.author.id)+1)
        slashes = slash_dic[ctx.author.id]
        description += f'\n**Your Position:**\n• **{position}** · <@{ctx.author.id}> · {slashes} {pl(slashes)}'
    await ctx.respond(embed=titledMessage("Kazuha Slash Leaderboard", description))

@bot.event
async def on_message(message):
     if regexPattern.match(message.content.lower()):
        if message.author.id in slash_dic:
            slash_dic[message.author.id] += 1
        else:
            slash_dic[message.author.id] = 1

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

def errorMessage(errorMessage: str):
    embedVar = discord.Embed(description=errorMessage, color=0xed4245)
    return embedVar

def titledMessage(embedTitle: str, embedBody: str):
    embedVar = discord.Embed(title=embedTitle, description=embedBody, color=0x5c9183)
    embedVar.set_thumbnail(url='https://cdn.discordapp.com/attachments/838507755915837440/988883937013157940/unknown.png')
    embedVar.set_footer(text='Powered and provided by GateKeeeper.', icon_url='https://imgur.com/9ubUKxY.png')
    return embedVar

def exit_handler():
    with open(file_path, 'wb') as f:
        pickle.dump(slash_dic, f)

def ordinaltg(n):
    return str(n) + {1: 'st', 2: 'nd', 3: 'rd'}.get(4 if 10 <= n % 100 < 20 else n % 10, "th")

def pl(n):
    if n > 1:
        return 'slashes'
    return 'slash'

atexit.register(exit_handler)
bot.run(kazuConfig.discordKey)

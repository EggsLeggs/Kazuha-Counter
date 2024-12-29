import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashCommandOptionType, SlashContext, utils
from datetime import datetime
import sqlite3
import kazuConfig
#------------------------------------------------------------------------------#
guild_ids = [836722051980066856]
fmt = '%Y-%m-%d %H:%M:%S'
#------------------------------------------------------------------------------#
description = "This bot is running to count kazuha slashes"
intents = discord.Intents.default()
activity = discord.Activity(type=discord.ActivityType.watching, name="discord.gg/kazuhamains")
bot = commands.Bot(command_prefix="KC$", activity=activity, description=description, intents=intents)
slash = SlashCommand(bot, sync_commands = False)
#------------------------------------------------------------------------------#

@bot.event
async def on_ready():
    print('Ready')

@slash.slash(name="leaderboard", description = 'Gets The Kazuha Slash Leaderboard.', guild_ids=guild_ids)
async def leaderboard(ctx : SlashContext):
    AddIfNotExist(ctx.author.id)
    sqliteConnection = sqlite3.connect('kazucount.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    sqlite_select_query = '''SELECT userID from LevelTable ORDER BY totalMessages DESC'''
    cursor.execute(sqlite_select_query)
    userIDs = cursor.fetchall()
    lbTitleText = ""
    for i in range (3):
        lbTitleText = lbTitleText+"**"+ord(i+1)+".  **<@"+str(userIDs[i][0])+"> - **"+str(getUserMessages(userIDs[i][0]))+"** Messages \n"
    embed = discord.Embed(description = lbTitleText, color=0xa6f2cb)
    embed.set_author(name= "Kazuha Slash Leaderboard", icon_url = ctx.guild.icon_url)
    embed.set_footer(text="Your rank is: " + str(getUserRank(ctx.author.id)+1))
    await ctx.send(embeds=[embed])

def getUserMessages(userID):
    sqliteConnection = sqlite3.connect('kazucount.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    sqlite_select_query = '''SELECT totalMessages from LevelTable where userID = {}'''.format(userID)
    cursor.execute(sqlite_select_query)
    messagecount = cursor.fetchone()
    cursor.close()
    sqliteConnection.close()
    return messagecount[0]

@bot.event
async def on_message(message):
    if (message.author.bot) or (message.type == 20) or ("kazuhaslash" not in ((message.content).lower()).replace(" ", "")) or (message.channel.id != 858959824719708191):
        return
    else:
        AddIfNotExist(message.author.id)
        sqliteConnection = sqlite3.connect('kazucount.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_select_query = '''SELECT dateLast,totalMessages from LevelTable where userID = {}'''.format(message.author.id)
        cursor.execute(sqlite_select_query)
        result = cursor.fetchone()
        s2 = result[0]
        cursor.close()
        sqliteConnection.close()
        s1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d1 = datetime.strptime(s1, fmt)
        d2 = datetime.strptime(s2, fmt)
        if ((d1-d2).seconds) > 5:
            sqliteConnection = sqlite3.connect('kazucount.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sql_update_query = '''Update LevelTable set totalMessages = {} where userID = "{}"'''.format(result[1]+1,message.author.id)
            cursor.execute(sql_update_query)
            sqliteConnection.commit()
            cursor.close()
            sqliteConnection.close()
    

def ord(n):
    return str(n)+("th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th"))

def AddIfNotExist(missingID):
    sqliteConnection = sqlite3.connect('kazucount.db')
    cursor = sqliteConnection.cursor()
    cursor.execute(''' insert or ignore into LevelTable(userID,dateLast,totalMessages)
                        VALUES(?,?,?) ''',(missingID,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),1))
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()
        
def getUserRank(userID):
    sqliteConnection = sqlite3.connect('kazucount.db')
    cursor = sqliteConnection.cursor()
    print("Connected to SQLite")
    sqlite_select_query = '''SELECT userID from LevelTable ORDER BY totalMessages DESC'''
    cursor.execute(sqlite_select_query)
    tdusers = cursor.fetchall()
    cursor.close()
    sqliteConnection.close()
    users = []
    for i in range(len(tdusers)):
        users.append(tdusers[i][0])
    return (users.index(userID))

#------------------------------------------------------------------------------#
bot.run(kazuConfig.discordKey)


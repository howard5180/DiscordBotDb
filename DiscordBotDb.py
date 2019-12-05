import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import sqlcommands as sqlc

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hi(ctx):
    await ctx.send("Hi")

@bot.command(aliases=["behemoth","bhm"])
async def behe(ctx, *a):
    i = 0
    joinedInput = " ".join(a)
    filteredInput = sqlc.filterInput(joinedInput)
    inputWordArray = filteredInput.split()

    attributesArray = sqlc.matchWeaponAttributes(inputWordArray)
    for key, content in attributesArray.items():
        if (content):
            i+=1

    if (i > 1):
        queryResults = sqlc.fetchBehemothByTypeDB(attributesArray)
    else:
        queryResults = sqlc.fetchBehemothDB(filteredInput)

    if (len(queryResults) > 0):
        embed = sqlc.behemothEmbedGenerator(queryResults, filteredInput)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Behemoth not found.")


@bot.command(aliases=["weap","weapon"])
async def wep(ctx, *a):
    joinedInput = " ".join(a)
    filteredInput = sqlc.filterInput(joinedInput)
    queryResults = sqlc.fetchWeaponDB(filteredInput)

    if (len(queryResults) == 1):
        embed = sqlc.weaponEmbed(queryResults)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Behemoth not found.")

@bot.command(aliases=["armour","arm"])
async def armor(ctx, *a):
    joinedInput = " ".join(a)
    filteredInput = sqlc.filterInput(joinedInput)
    queryResults = sqlc.fetchArmorDB(filteredInput)

    if (len(queryResults) == 4):
        embed = sqlc.armorEmbed(queryResults)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Behemoth not found.")

@bot.command()
async def magi(ctx, *a):
    joined = " ".join(a)
    filteredInput = sqlc.filterInput(joined)
    queryResults = sqlc.fetchMagiDB(filteredInput)

    if (len(queryResults) > 0):
        embed = sqlc.magiEmbedGenerator(queryResults, filteredInput)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Magi not found.")
    
@armor.error
async def armor_on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="The correct syntax is:", colour=discord.Colour(0xff0000), description="`?armor [Behemoth's name]`")
        await ctx.send(embed=embed)
    raise error

@wep.error
async def weapon_on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="The correct syntax is:", colour=discord.Colour(0xff0000), description="`?weapon [Behemoth's name]`")
        await ctx.send(embed=embed)
    raise error

@behe.error
async def behemoth_on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="The correct syntax is:", colour=discord.Colour(0xff0000), description="`?behemoth [Behemoth's name]`")
        await ctx.send(embed=embed)
    raise error

@magi.error
async def magi_on_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="The correct syntax is:", colour=discord.Colour(0xff0000), description="`?magi [Magi's name]`")
        await ctx.send(embed=embed)
    raise error

#host bot
bot.run(os.environ["ACCESS_TOKEN"])
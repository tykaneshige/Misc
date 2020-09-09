import asyncio
import discord
import random
import youtube_dl

from discord.ext import commands

token = 'Insert Token Here'

client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Bot Commands
@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

@bot.command()
async def gimme(ctx):
    quote = open('gimme.txt').read()
    await ctx.send(quote)

@bot.command()
async def quote(ctx):
    responses = open('quotes.txt').read().splitlines()
    random.seed(a=None)
    response = random.choice(responses)
    await ctx.send(response)

@bot.command()
async def goat(ctx):
    with open('images/Joe_Kelly.png', 'rb') as fp:
        goat = discord.File(fp, spoiler=True)
        await ctx.send(file=goat)

@bot.command()
async def whoami(ctx):
    with open('images/Me.png', 'rb') as fp:
        me = discord.File(fp)
        await ctx.send(file=me)

@bot.command()
async def dc(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def exit(ctx):
    await ctx.send('Shutting down.')
    await bot.close()

    if bot.is_closed():
        print('Bot succesfully shut down.')
    else:
        print('Bot did not properly shut down.')

# Bot Events
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(token)
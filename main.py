import discord
import os
from discord.ext import commands, tasks


intents = discord.Intents.all()
client = discord.Client(intents=intents)
token = os.getenv('TOKEN')
channel = os.getenv('CHANNEL')
bot = commands.Bot(command_prefix='!')

@client.event
async def on_message(message):
    channel = client.get_channel(channel)

        if not message.guild:
        await message.channel.send('not today mate')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
    
client.run(token) 
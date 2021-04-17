
from decouple import config
import discord
from discord.ext import commands

token = config('TOKEN')
bot = commands.Bot(command_prefix="$", case_insensitive=True)


@bot.command()
async def stonkssupportbot(ctx, *args):
    if len(args) > 0:
        if len(args) == 3:
            if args[0].lower() == "back" and args[1].lower() == "me" and args[2].lower() == "up":
                await ctx.reply("you are right and your opponents are wrong")

    if len(args) == 0:
        await ctx.reply("wut?")

@bot.event
async def on_message(message):
    if(message.author.id == 550616372120387585) and message.content.lower().find('gme') != -1:
        await message.channel.send("gotcha")

bot.run(token) 
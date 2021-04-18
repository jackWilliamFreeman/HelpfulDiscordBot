import finnhub
import os
from  dotenv import load_dotenv
import discord
from discord.ext import commands
import boto3
from keep_alive import keep_alive

load_dotenv()
#token = os.getenv('TOKEN')
token = os.getenv('TEST_TOKEN')
#stonks_bot_id= int(os.getenv('STONKS_BOT_ID'))
stonks_bot_id= int(os.getenv('TEST_STONKS_BOT_ID'))
finnhub_token = os.getenv("FINNHUB_TOKEN")
aws_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('REGION')

bot = commands.Bot(command_prefix="$", case_insensitive=True)
finnhub_client = finnhub.Client(api_key=finnhub_token)

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=aws_region
     )

table = dynamodb.Table('last_price')
initial_buyin = 115


@bot.event
async def on_ready():
    print("I'm ready.")

#command entry
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
    if(message.author.id == stonks_bot_id):
        dem_gains = get_gains()
        old_gains = get_last_gains()
        save_gains(dem_gains)
        if dem_gains > old_gains:
            await message.channel.send("Congratulations Ian on your winning Ape Strategy, you have improved on last time!")
        if dem_gains < old_gains:
            await message.channel.send("Oh no Ian has lost some gains and sits at {}%!\r\n it's not too late you can get help at: https://www.lifeline.org.au/".format(dem_gains))
        if dem_gains == old_gains:
            await message.channel.send("Ian's gainst haven't changed, breathe easy kids (still at {}%).".format(dem_gains))

def get_gains():
     quote = finnhub_client.quote('GME')
     current_price = quote["c"]
     dem_gains = round((current_price/initial_buyin - 1) * 100,2)
     return dem_gains

def get_last_gains():
    resp = table.get_item(
    Key={
        'PK':'last_gains'
    }
)
    return float(resp['Item']['gains'])

def save_gains(gains):
    table.put_item(
        Item={
        'PK': 'last_gains',
        'gains': str(gains),
    }
)

keep_alive()
bot.run(token) 

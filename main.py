import finnhub
import os
from  dotenv import load_dotenv
import discord
from discord.ext import commands
import boto3
import time
from keep_alive import keep_alive


load_dotenv()
token = os.environ['TOKEN']
stonks_bot_id= int(os.environ['STONKS_BOT_ID'])
finnhub_token = os.environ["FINNHUB_TOKEN"]
aws_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['REGION']

bot = commands.Bot(command_prefix="!", case_insensitive=True)
finnhub_client = finnhub.Client(api_key=finnhub_token)

dynamodb = boto3.resource('dynamodb',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
    region_name=aws_region
     )

table = dynamodb.Table('last_price')
initial_buyin = 115.92


@bot.event
async def on_ready():
    print("I'm ready.")
    print(f'{bot.user.name} has connected to discord!')
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching, 
                          name = 'Porn on Disney+'))

@bot.event
async def on_message(message):
    if(message.author.id == stonks_bot_id) and message.content.startswith('GME YOLO'):
        dem_gains = await get_gains(message)
        old_gains = get_last_gains()
        save_gains(dem_gains)
        if dem_gains > old_gains:
            await message.channel.send("Congratulations Ian on your winning Ape Strategy, you have improved on last time!")
        if dem_gains < old_gains:
            await message.channel.send("Oh no Ian has lost some gains and sits at {}%!\r\n it's not too late you can get help at: https://gaaustralia.org.au/".format(dem_gains))
        if dem_gains == old_gains:
            await message.channel.send("Ian's gains haven't changed, breathe easy kids (still at {}%).".format(dem_gains))

async def get_gains(message):
     try:
        quote = finnhub_client.quote('GME')
     except:
        time.sleep(1)
        try:
            quote = finnhub_client.quote('GME')
        except:
            await message.channel.send("I can't determine if Ian is up or down. It may be time to panic.")
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

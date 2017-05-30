from discord.ext import commands
import discord
import json, asyncio

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

initial_extensions = [
    'cogs.reddit',
    'cogs.raid',
    'cogs.aqual.aqual',
    'cogs.roll',
    'cogs.chucknorris',
    'cogs.youtube',
    'cogs.trivia.trivia',
    'cogs.blackjack',
    'cogs.8ball',
    'cogs.music'
]

help_attrs = dict(hidden=True)
prefix = ['!', '\N{HEAVY EXCLAMATION MARK SYMBOL}']
bot = commands.Bot(command_prefix=prefix, pm_help=None, help_attrs=help_attrs)

def load_credentials():
    with open('credentials.json') as f:
        return json.load(f)

@bot.event
async def on_read():
    print("Client logged in")

if __name__ == '__main__':
    credentials = load_credentials()

    token = credentials['BOT_TOKEN']
    bot.CLIENT_ID = credentials['BOT_CLIENT_ID']
    bot.CLIENT_SECRET = credentials['BOT_CLIENT_SECRET']
    bot.PRAW_CLIENT_ID = credentials['PRAW']['CLIENT_ID']
    bot.PRAW_CLIENT_SECRET = credentials['PRAW']['CLIENT_SECRET']
    bot.PRAW_USER_AGENT = credentials['PRAW']['USER_AGENT']
    bot.SHIVTR_HEADERS = credentials['SHIVTR']['HEADERS']
    bot.SHIVTR_DATA = credentials['SHIVTR']['DATA']
    bot.SHIVTR_URL = credentials['SHIVTR']['URL']
    bot.TRIVIA_ROOM_ID = credentials['TRIVIA_ROOM_ID']
    bot.BLACKJACK_ROOM_ID = credentials['BLACKJACK_ROOM_ID']
    bot.RANDOM_ROOM_ID = credentials['RANDOM_ROOM_ID']

    bot.remove_command('help')

    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(token)

from discord.ext import commands
import discord
from cogs.utils import checks
import aiohttp
import asyncio
import pickle

class Twitch:


    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.task = self.bot.loop.create_task(self.check_streamers())

    def __unload(self):
        self.session.close()
        self.task.cancel()

    def read(self):
        with open('cogs/twitch/livestreams.txt', 'rb') as f:
            return pickle.load(f)

    def write(self, livestreams):
        with open('cogs/twitch/livestreams.txt', 'wb') as f:
            pickle.dump(livestreams, f)

    @commands.command()
    @checks.is_owner()
    async def disablealerts(self):
        self.task.cancel()
        await self.bot.say('Twitch alerts have been disabled.')

    @commands.command()
    @checks.is_owner()
    async def enablealerts(self):
        self.task = self.bot.loop.create_task(self.check_streamers())
        await self.bot.say('Twitch alerts have been enabled.')

    @commands.command()
    async def removetwitch(self, message: str):
        livestreams = self.read()
        if message.lower() in livestreams:
            livestreams.pop(message, 0)
            self.write(livestreams)
            await self.bot.say(message + ' has been removed from the notify list.')
        else:
            await self.bot.say(message + ' is not on the notify list.')

    @commands.command()
    async def addtwitch(self, message: str):
        livestreams = self.read()
        if message in livestreams:
            await self.bot.say(message + ' is already on the notify list.')
        else:
            livestreams[message.lower()] = 'offline'
            self.write(livestreams)
            await self.bot.say(message + ' has been added to the notify list.')

    @commands.command()
    async def listtwitch(self):
        livestreams = self.read()
        string_list = '\n'.join(livestreams.keys())
        number = str(len(livestreams.keys()))
        await self.bot.say(string_list)


    async def notify_live(self, streamer):
        url = 'https://api.twitch.tv/kraken/streams/' + streamer + '?client_id=' + self.bot.TWITCH_CLIENT_ID
        async with self.session.get(url) as r:
            channel = self.bot.get_channel(self.bot.TWITCH_ALERT_CHANNEL)
            link = 'https://twitch.tv/' + streamer
            msg = streamer + ' has gone live!'
            js = await r.json()
            livestreams = self.read()
            print(livestreams[streamer] == 'offline')
            if js['stream'] and (livestreams[streamer] == 'offline'):
                print(streamer + ' has gone live')
                livestreams[streamer] = 'online'
                self.write(livestreams)
                await self.bot.send_message(channel, msg)
                await self.bot.send_message(channel, link)
            elif js['stream'] is None and (livestreams[streamer] == 'online'):
                print(streamer + ' has gone offline')
                livestreams[streamer] = 'offline'
                self.write(livestreams)
            else:
                print(streamer + ' is already offline or online')



    async def check_streamers(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)
        while not self.bot.is_closed:
            print(1)
            livestreams = self.read()
            for key in livestreams.keys():
              await self.notify_live(key)
            await asyncio.sleep(45)

def setup(bot):
    bot.add_cog(Twitch(bot))

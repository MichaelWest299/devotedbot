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

    def __unload(self):
        self.session.close()

    def read(self):
        with open('cogs/twitch/livestreams.txt', 'rb') as f:
            return pickle.load(f)

    def write(self, livestreams):
        with open('cogs/twitch/livestreams.txt', 'wb') as f:
            pickle.dump(livestreams, f)

    @commands.command()
    @checks.is_owner()
    async def disablealerts(self):
        try:
            self.task.cancel()
            await self.bot.say('Twitch alerts have been disabled.')
        except AttributeError:
            await self.bot.say('Twitch alerts are already disabled.')


    @commands.command()
    @checks.is_owner()
    async def enablealerts(self):
        try:
            self.task.cancel()
            self.task = self.bot.loop.create_task(self.check_streamers())
            await self.bot.say('Twitch alerts are already enabled.')
        except AttributeError:
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
        string_list = '\n'.join('[' + item + ']' + '(https://www.twitch.tv/' + item + ')' for item in livestreams.keys())
        number = str(len(livestreams.keys()))
        embed = discord.Embed(colour=0x8080ff, title='__Streams__', description=string_list)
        await self.bot.say(embed=embed)


    async def notify_live(self, streamer):
        url = 'https://api.twitch.tv/kraken/streams/' + streamer + '?client_id=' + self.bot.TWITCH_CLIENT_ID
        async with self.session.get(url) as r:
            channel = self.bot.get_channel(self.bot.TWITCH_ALERT_CHANNEL)
            link = 'https://twitch.tv/' + streamer
            msg = streamer + ' has gone live!'
            js = await r.json()
            livestreams = self.read()
            if js['stream'] and (livestreams[streamer] == 'offline'):
                livestreams[streamer] = 'online'
                self.write(livestreams)
                await self.bot.send_message(channel, msg)
                await self.bot.send_message(channel, link)
            elif js['stream'] is None and (livestreams[streamer] == 'online'):
                livestreams[streamer] = 'offline'
                self.write(livestreams)
            else:
                return



    async def check_streamers(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)
        while not self.bot.is_closed:
            livestreams = self.read()
            for key in livestreams.keys():
              await self.notify_live(key)
            await asyncio.sleep(45)

def setup(bot):
    bot.add_cog(Twitch(bot))

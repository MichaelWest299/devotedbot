from discord.ext import commands
import discord
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


    async def notify_live(self, streamer):
        url = 'https://api.twitch.tv/kraken/streams/' + streamer + '?client_id=p7k19ow79cnir9695tlo3f800gabrj'
        async with self.session.get(url) as r:
            channel = self.bot.get_channel('314866130600853516')
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
            await asyncio.sleep(30)


def setup(bot):
    bot.add_cog(Twitch(bot))

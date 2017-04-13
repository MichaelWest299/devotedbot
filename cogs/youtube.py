from discord.ext import commands
import discord
import urllib.parse
from bs4 import BeautifulSoup
import aiohttp


class Youtube:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    @commands.command()
    async def youtube(self, *, message: str):
        query = urllib.parse.quote(message)
        url = "https://www.youtube.com/results?search_query=" + query
        async with self.session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            vid = soup.find(attrs={'class': 'yt-uix-tile-link'})
            await self.bot.say('https://www.youtube.com' + vid['href'])


def setup(bot):
    bot.add_cog(Youtube(bot))

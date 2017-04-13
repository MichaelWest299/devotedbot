from discord.ext import commands
import discord
from bs4 import BeautifulSoup
import aiohttp


class Wareffort:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    @commands.command()
    async def wareffort(self):
        url_wareffort = 'http://nostalri.us/anathema'
        async with self.session.get(url_wareffort) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            tagged_text = soup.find_all("span", {'class': 'r'})[-1].get_text()
            await self.bot.say("Current War Effort Progress: " + tagged_text)


def setup(bot):
    bot.add_cog(Wareffort(bot))

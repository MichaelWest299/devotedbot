from discord.ext import commands
import discord
import aiohttp

class Chucknorris:


    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    @commands.command()
    async def chucknorris(self):
        url = 'http://api.icndb.com/jokes/random'
        async with self.session.get(url) as r:
            js = await r.json()
            joke_string = js['value']['joke']
            new_str = str.replace(joke_string, "&quot;", "\"");
            await self.bot.say(new_str)


def setup(bot):
    bot.add_cog(Chucknorris(bot))

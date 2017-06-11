from discord.ext import commands
import discord
import aiohttp

class Define:


    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    @commands.command()
    async def define(self, word: str):
        url = 'http://api.wordnik.com:80/v4/word.json/' + word.lower() + '/definitions?limit=10&includeRelated=true&sourceDictionaries=all&useCanonical=false&includeTags=false&api_key=' + self.bot.WORDNIK_API_KEY

        try:
            async with self.session.get(url) as r:
                js = await r.json()
                definition = js[0]['text']
                await self.bot.say(definition)
        except (IndexError, KeyError):
            await self.bot.say('Sorry, no definiton has been found for ' + word + '.')

def setup(bot):
    bot.add_cog(Define(bot))

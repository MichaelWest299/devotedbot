from discord.ext import commands
import discord
import youtube_dl
from ctypes.util import find_library
from discord import opus
import urllib.parse
from bs4 import BeautifulSoup
import aiohttp

class Music:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    if not opus.is_loaded():
        opus.load_opus(find_library('opus'))

    @commands.command(pass_context=True)
    async def yt(self, ctx, *, message: str):
        if(ctx.message.channel == self.bot.get_channel('312589826291400706')):
            await self.bot.say(opus.is_loaded())
            query = urllib.parse.quote(message)
            query_url = "https://www.youtube.com/results?search_query=" + query
            async with self.session.get(query_url) as response:
                soup = BeautifulSoup(await response.text(), "html.parser")
                vid = soup.find(attrs={'class': 'yt-uix-tile-link'})
                play_url = 'https://www.youtube.com' + vid['href']
            music_channel = self.bot.get_channel('312592653223198743')
            voice = await self.bot.join_voice_channel(music_channel)
            player = await voice.create_ytdl_player(play_url)
            player.start()

def setup(bot):
    bot.add_cog(Music(bot))

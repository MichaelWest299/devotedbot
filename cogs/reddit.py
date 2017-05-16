from discord.ext import commands
import discord
import praw
import random
from prawcore import NotFound


class Reddit:

    def __init__(self, bot):
        self.bot = bot

    def sub_exists(self, sub):
        exists = True
        try:
            reddit = praw.Reddit(client_id=self.bot.PRAW_CLIENT_ID,
                                 client_secret=self.bot.PRAW_CLIENT_SECRET,
                                 user_agent=self.bot.PRAW_USER_AGENT)
            reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
        return exists

    @commands.command()
    async def r(self, sub: str):
        if self.sub_exists(sub):
            content_list = []
            reddit = praw.Reddit(client_id=self.bot.PRAW_CLIENT_ID,
                                 client_secret=self.bot.PRAW_CLIENT_SECRET,
                                 user_agent=self.bot.PRAW_USER_AGENT)
            for submission in reddit.subreddit(sub).hot(limit=128):
                content_list.append(submission.url)
            await self.bot.say(random.choice(content_list))
        else:
            await self.bot.say('Sorry that subreddit does not exist')

def setup(bot):
    bot.add_cog(Reddit(bot))

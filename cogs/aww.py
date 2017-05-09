from discord.ext import commands
import discord
import praw
import random

class Aww:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def aww(self):
        list_aww = []
        reddit = praw.Reddit(client_id=self.bot.PRAW_CLIENT_ID,
                             client_secret=self.bot.PRAW_CLIENT_SECRET,
                             user_agent=self.bot.PRAW_USER_AGENT)

        for submission in reddit.subreddit('aww').hot(limit=128):
            list_aww.append(submission.url)

        await self.bot.say(random.choice(list_aww))


def setup(bot):
    bot.add_cog(Aww(bot))

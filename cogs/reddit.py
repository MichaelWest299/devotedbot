from discord.ext import commands
import discord
import praw
import random


class Reddit:

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

    @commands.command()
    async def meme(self):
        list_dankmemes = []
        reddit = praw.Reddit(client_id=self.bot.PRAW_CLIENT_ID,
                             client_secret=self.bot.PRAW_CLIENT_SECRET,
                             user_agent=self.bot.PRAW_USER_AGENT)

        for submission in reddit.subreddit('memes').hot(limit=128):
            list_dankmemes.append(submission.url)

        await self.bot.say(random.choice(list_dankmemes))


def setup(bot):
    bot.add_cog(Reddit(bot))

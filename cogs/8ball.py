from discord.ext import commands
import discord
import random

class Eightball:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ask(self, ctx, *, message: str):
        choices = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]
        description = ':8ball:' + random.choice(choices) + ':8ball:'
        em = discord.Embed(description=description, colour=0x808080)
        await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Eightball(bot))

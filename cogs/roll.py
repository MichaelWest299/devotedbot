from discord.ext import commands
import discord
from random import randint


class Roll:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, number: int = None):
        member = ctx.message.author.name
        if number is None:
            await self.bot.say(member + ' rolls ' + str(randint(1, 100)) + ' (1-100)')
        else:
            await self.bot.say(member + ' rolls ' + str(randint(1, number)) + ' (1-' + str(number) + ')')


def setup(bot):
    bot.add_cog(Roll(bot))

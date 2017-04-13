from discord.ext import commands
import discord
import pickle


class Aqual:

    def __init__(self, bot):
        self.bot = bot

    def read(self):
        with open('aqual.txt', 'rb') as f:
            return pickle.load(f)

    def write(self, list):
        with open('aqual.txt', 'wb') as f:
            pickle.dump(list, f)

    @commands.command(pass_context=True)
    async def aqualready(self, ctx):
        list = self.read()
        member = ctx.message.author.name
        if member in list:
            await self.bot.say(member + ' is already on the Aqual Quintessence list')
        else:
            await self.bot.say(member + ' has been added to the Aqual Quintessence list')
            list.append(member)
        self.write(list)

    @commands.command(pass_context=True)
    async def aqualremove(self, ctx):
        list = self.read()
        member = ctx.message.author.name
        if member in list:
            list.remove(member)
            await self.bot.say(member + ' has been removed from the Aqual Quintessence list')
        else:
            await self.bot.say(member + ' is not on the Aqual Quintessence list')
        self.write(list)

    @commands.command()
    async def aqual(self):
        list = self.read()
        string_list = ', '.join(list)
        number = str(len(list))
        await self.bot.say('We have ' + number + ' Aqual Quintessence ready for next raid: ' + string_list)


def setup(bot):
    bot.add_cog(Aqual(bot))

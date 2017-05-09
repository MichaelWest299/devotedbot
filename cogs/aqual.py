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
    async def aqualclear(self, ctx):
        if(ctx.message.author.name == 'Globalelite'):
            list = []
            self.write(list)
            embed = discord.Embed(colour=0x00FF00, description='Aqual list cleared.')
        else:
            raid_string = 'There are currently no events scheduled.'
            embed = discord.Embed(colour=0xFF0000, description='You are not permitted to do that.')
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True)
    async def aqualready(self, ctx):
        list = self.read()
        author = ctx.message.author
        member = ctx.message.author.name
        if member in list:
            description = 'You are already on the Aqual Quintessence list'
            embed = discord.Embed(colour=0xFF0000, description=description)
        else:
            list.append(member)
            description = 'You been added to the Aqual Quintessence list'
            embed = discord.Embed(colour=0x00FF00, description=description)

        embed.set_author(name=member, icon_url=author.avatar_url)
        await self.bot.say(embed=embed)
        self.write(list)

    @commands.command(pass_context=True)
    async def aqualremove(self, ctx):
        list = self.read()
        author = ctx.message.author
        member = ctx.message.author.name
        if member in list:
            list.remove(member)
            description = 'You have been removed from the Aqual Quintessence list'
            embed = discord.Embed(colour=0x00FF00, description=description)
        else:
            description = 'You are not on the Aqual Quintessence list'
            embed = discord.Embed(colour=0xFF0000, description=description)

        embed.set_author(name=member, icon_url=author.avatar_url)
        await self.bot.say(embed=embed)

        self.write(list)

    @commands.command()
    async def aqual(self):
        list = self.read()
        string_list = ', '.join(list)
        number = str(len(list))
        title = 'We have ' + number + ' Aqual Quintessence ready for next raid:'
        embed = discord.Embed(colour=0x00FF00, description=string_list, title=title)
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Aqual(bot))

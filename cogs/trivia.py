from discord.ext import commands
import discord
import aiohttp
import html
import random
import pickle
import operator


class Trivia:
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    def read(self):
        with open('highscores.txt', 'rb') as f:
            return pickle.load(f)

    def write(self, highscores):
        with open('highscores.txt', 'wb') as f:
            pickle.dump(highscores, f)

    async def handle_response(self, ctx, highscores, results, award):
        reply = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel, timeout=20.0)
        if reply is None:
            highscores[ctx.message.author.name] -= 1
            description = html.unescape('You took too long, the correct answer was ' + results['correct_answer'].strip())
            embed = discord.Embed(colour=0xFF0000, description=description)
            text =  ctx.message.author.name + ' has lost 1 point and' + ' now has a score of ' + str(highscores[ctx.message.author.name])
        elif reply.content.lower() == html.unescape(results['correct_answer'].strip().lower()):
            highscores[ctx.message.author.name] += award
            description = html.unescape(results['correct_answer'].strip() + ' is the correct answer, woo!')
            embed = discord.Embed(colour=0x00FF00, description=description)
            text =  ctx.message.author.name + ' was awarded ' + str(award) + ' point(s) and now has a score of ' + str(highscores[ctx.message.author.name])
        elif reply.content == '!trivia':
            return
        else:
            highscores[ctx.message.author.name] -= 1
            description = html.unescape(reply.content + ' is the incorrect answer. The correct answer was ' + results['correct_answer'])
            embed = discord.Embed(colour=0xFF0000, description=description)
            text = ctx.message.author.name + ' has lost 1 point and' + ' now has a score of ' + str(highscores[ctx.message.author.name])
        self.write(highscores)
        embed.set_footer(text=text, icon_url=ctx.message.author.avatar_url)
        return await self.bot.say(embed=embed)

    def init_new_player(self, ctx, highscores):
        if not (ctx.message.author.name in highscores):
            highscores[ctx.message.author.name] = 0

    def calc_reward(self, results):
        if(results['difficulty'] == 'easy'):
            award = 1
        elif(results['difficulty'] == 'medium'):
            award = 2
        else:
            award = 3
        return award


    @commands.command(pass_context=True)
    async def clearhighscores(self, ctx):
        if(ctx.message.author.name == 'Globalelite'):
            highscores = {}
            self.write(highscores)
            await self.bot.say('Highscores cleared.')
        else:
            await self.bot.say('You are not permitted to do that.')



    @commands.command()
    async def highscores(self):

        highscores = self.read()
        if not highscores:
            description = 'There are no highscores yet.'
            embed = discord.Embed(colour=0xFF0000, description=description)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(colour=0x00FF00, title='__Trivia Highscores__')
            sorted_highscores = sorted(highscores.items(), reverse=True, key=lambda x: x[1])
            top_five = sorted_highscores[:5]
            user_list = []
            score_list = []
            for x in top_five:
                user_list.append(x[0])
                score_list.append(str(x[1]))
            string_users = '\n'.join(user_list)
            string_scores = '\n'.join(score_list)
            embed.add_field(name='Player', value=string_users, inline=True)
            embed.add_field(name='Score', value=string_scores, inline=True)
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def trivia(self, ctx):

        if(ctx.message.channel == self.bot.get_channel('311063195164868612')):
            highscores = self.read()
            self.init_new_player(ctx, highscores)
            url = 'https://opentdb.com/api.php?amount=1'
            async with self.session.get(url) as r:
                js = await r.json()
                results = js['results'][0]
                question = results['question']

                award = self.calc_reward(results)

                type = results['type']
                if(type == "boolean"):
                    title = html.unescape(results['difficulty'].capitalize() + ': ' + question)
                    description = "True or False."
                    embed = discord.Embed(colour=0xFF9900, description=description, title=title)
                    await self.bot.say(embed=embed)
                    await self.handle_response(ctx, highscores, results, award)

                else:
                    answers = []
                    answers.append(html.unescape(results['correct_answer'].strip()))
                    for i in results['incorrect_answers']:
                        answers.append(html.unescape(i.strip()))
                    shuffled_answers = random.sample(answers, len(answers))
                    string_list = '\n'.join(shuffled_answers)

                    title = html.unescape(results['difficulty'].capitalize() + ': ' + question)
                    description = html.unescape(string_list)
                    embed = discord.Embed(colour=0xFF9900, description=description, title=title)
                    await self.bot.say(embed=embed)
                    await self.handle_response(ctx, highscores, results, award)

        else:
            await self.bot.say("Please use the trivia channel.")


def setup(bot):
    bot.add_cog(Trivia(bot))

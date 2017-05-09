from discord.ext import commands
import discord
import json
import aiohttp

# define globals for cards
SUITS = {'CLUBS': ':clubs:', 'SPADES': ':spades:',
         'HEARTS': ':hearts:', 'DIAMONDS': ':diamonds:'}
RANKS = ('ACE', '2', '3', '4', '5', '6', '7',
         '8', '9', '10', 'JACK', 'QUEEN', 'KING')
VALUES = {'ACE': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
          '8': 8, '9': 9, '10': 10, 'JACK': 10, 'QUEEN': 10, 'KING': 10}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if(self.rank == '10'):
            return "| %s %s | " % (self.rank, SUITS[self.suit])
        else:
            return "| %s %s | " % (self.rank[:1].capitalize(), SUITS[self.suit])

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

class Hand:
    def __init__(self):
        self.player_hand = []

    def __str__(self):
        s = ''
        for c in self.player_hand:
            s = s + str(c) + ' '
        return s

    def add_card(self, card):
        self.player_hand.append(card)
        return self.player_hand

    def get_first_card(self):
        return self.player_hand[0]

    def get_value(self):
        value = 0
        for card in self.player_hand:
            rank = card.get_rank()
            value = value + VALUES[rank]
        for card in self.player_hand:
            rank = card.get_rank()
            if rank == 'ACE' and value <= 11:
                value += 10
        return value

class Blackjack:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    async def get_deck_id(self):
        url = 'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6'
        async with self.session.get(url) as r:
            js = await r.json()
            deck_id = js['deck_id']
            return deck_id

    async def stand(self, ctx, card_index, players, cards):
        while (players[0].get_value() < 17):
            h = Card(cards[card_index]['suit'],
                     cards[card_index]['value'])
            card_index += 1
            players[0].add_card(h)

        dealer_cards = str(players[0]) + ' **' + str(players[0].get_value()) + '**'
        embed = discord.Embed(colour=0x00FF00)
        embed.add_field(name='Dealer', value=dealer_cards, inline=True)
        await self.bot.say(embed=embed)

        if players[0].get_value() > 21:
            embed = discord.Embed(colour=0x00FF00, description= ctx.message.author.name + " wins! Dealer busted with " + ' **' + str(players[0].get_value()) + '**')
        elif players[0].get_value() > players[1].get_value():
            embed = discord.Embed(colour=0xFF0000, description="Dealer wins with " + ' **' + str(players[0].get_value()) + '**')
        elif players[0].get_value() == players[1].get_value():
            embed = discord.Embed(colour=0xFF0000, description="Tie! Dealer wins with " + ' **' + str(players[0].get_value()) + '**')
        elif players[0].get_value() < players[1].get_value():
            embed = discord.Embed(colour=0x00FF00, description=ctx.message.author.name + " wins with " + ' **' + str(players[1].get_value()) + '**')
        await self.bot.say(embed=embed)


    async def follow_up(self, ctx, card_index, players, cards):
        embed = discord.Embed(colour=0xFF9900, description='Hit or stand?')
        await self.bot.say(embed=embed)
        reply = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel, timeout=20.0)
        if reply is None:
            embed = discord.Embed(colour=0xFF0000, description=ctx.message.author.name + ' took too long. Standing...')
            await self.bot.say(embed=embed)
            await self.stand(ctx, card_index, players, cards)
        elif reply.content.lower() == 'hit':
            f = Card(cards[card_index]['suit'],
                     cards[card_index]['value'])
            players[1].add_card(f)
            card_index += 1
            user_cards = str(players[1]) + ' **' + str(players[1].get_value()) + '**'
            embed = discord.Embed(colour=0x00FF00)
            embed.add_field(name=ctx.message.author.name, value=user_cards, inline=True)
            await self.bot.say(embed=embed)
            if(players[1].get_value() > 21):
                embed = discord.Embed(colour=0xFF0000, description='Dealer wins! ' + ctx.message.author.name + ' busted with **' + str(players[1].get_value()) + '**')
                return await self.bot.say(embed=embed)
            elif(players[1].get_value() == 21):
                await self.stand(ctx, card_index, players, cards)
            else:
                return await self.follow_up(ctx, card_index, players, cards)

        elif reply.content.lower() == 'stand':
            await self.stand(ctx, card_index, players, cards)
        else:
            return await self.follow_up(ctx, card_index, players, cards)




    async def deal(self, ctx, num_players, cards):

        players = [Hand() for i in range(num_players)]
        card_index = 0
        for obj in players:

            x = Card(cards[players.index(obj)]['suit'],
                     cards[players.index(obj)]['value'])
            obj.add_card(x)

            g = Card(cards[players.index(obj) + num_players]['suit'],
                     cards[players.index(obj) + num_players]['value'])
            obj.add_card(g)
            card_index += 2

        dealer_card = str(players[0].get_first_card())
        user_cards = str(players[1]) + ' **' + str(players[1].get_value()) + '**'
        embed = discord.Embed(colour=0x00FF00)
        value = str(players[0].get_value())
        embed.add_field(name=ctx.message.author.name, value=user_cards, inline=False)
        embed.add_field(name='Dealer', value=dealer_card, inline=False)
        await self.bot.say(embed=embed)
        #player wins if they get 2 card 21 and dealer doesn't have blackjack
        dealer_cards = str(players[0]) + ' **' + str(players[0].get_value()) + '**'
        if players[1].get_value() == 21 and players[0].get_value() != 21:
            embed = discord.Embed(colour=0x00FF00)
            embed.add_field(name='Dealer', value=dealer_cards, inline=True)
            await self.bot.say(embed=embed)
            embed = discord.Embed(colour=0x00FF00, description=ctx.message.author.name + " wins with a blackjack!")
            await self.bot.say(embed=embed)

        elif(players[1].get_value() == 21 and players[0].get_value() == 21):
            embed = discord.Embed(colour=0x00FF00)
            embed.add_field(name='Dealer', value=dealer_cards, inline=True)
            await self.bot.say(embed=embed)
            embed = discord.Embed(colour=0xFF0000, description="Tie! Dealer wins with a blackjack!")
            await self.bot.say(embed=embed)
        else:
            await self.follow_up(ctx, card_index, players, cards)



    @commands.command(pass_context=True)
    async def blackjack(self, ctx):
        if(ctx.message.channel == self.bot.get_channel(self.bot.BLACKJACK_ROOM_ID)):
            num_players = 2
            deck_id = await self.get_deck_id()
            url = 'https://deckofcardsapi.com/api/deck/' + deck_id + '/draw/?count=' + str(num_players * 20)
            async with self.session.get(url) as r:
                js = await r.json()
                cards = js['cards']
                await self.deal(ctx, num_players, cards)
        else:
            await self.bot.say("Please use the blackjack channel.")






def setup(bot):
    bot.add_cog(Blackjack(bot))

from discord.ext import commands
import discord
import datetime
import iso8601
import pytz
import json
import aiohttp
import re

class Raid:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    async def get_token(self):
        headers = {"Content-Type": "application/json"}
        data = json.dumps(self.bot.SHIVTR_DATA)

        async with self.session.post(self.bot.SHIVTR_URL + 'users/sign_in.json', headers=headers, data=data) as r:
            captured_json = await r.json()
            authenticity_token = captured_json['user_session']['authentication_token']
            return authenticity_token

    async def get_data(self, data):
        authenticity_token = await self.get_token()
        async with self.session.get(self.bot.SHIVTR_URL + data + '.json?auth_token=' + authenticity_token) as r:
            js = await r.json()
            return js

    @commands.command()
    async def apps(self):
        apps_json = await self.get_data('site_applications')
        open_apps = []
        for i in apps_json['site_applications']:
            if(i['status'] == 'open'):
                for j in apps_json['game_classes']:
                    if (j['id'] == i['game_class_id']):
                        open_apps.append(i['name']+': '+j['name'])
        string_list = '\n'.join(open_apps)
        if not string_list:
            embed = discord.Embed(colour=0xFF0000, description='We have no open applications.')
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(colour=0x00FF00, description=string_list)
            embed.title = 'Applications'
            await self.bot.say(embed=embed)

    @commands.command()
    async def raid(self):
        now = iso8601.parse_date(datetime.datetime.now(pytz.timezone('Europe/Amsterdam')).replace(microsecond=0).isoformat())
        events_json = await self.get_data('events')
        for i in events_json['events']:
            if(iso8601.parse_date(i['date'])>now):
                event_id = i['event_id']
                for j in events_json['event_objects']:
                    if(j['id'] == event_id):
                        raid_string = iso8601.parse_date(i['date']).strftime('%a %d %B %H:%M') + '\nPlease [click here](' + self.bot.SHIVTR_URL + 'events/' + str(i['event_id']) + '?event_instance_id=' + str(i['id']) + ' \"' + j['name'] + '\") to sign up!'
                        embed = discord.Embed(colour=0x00FF00, description=raid_string)
                        embed.title = j['name']
                break
            else:
                raid_string = 'There are currently no events scheduled.'
                embed = discord.Embed(colour=0xFF0000, description=raid_string)

        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Raid(bot))

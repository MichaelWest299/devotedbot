from discord.ext import commands
import discord
import datetime
import iso8601
import pytz
import json
import aiohttp

class Raid:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)

    def __unload(self):
        self.session.close()

    async def get_token(self):
        headers = {"Content-Type": "application/json"}
        data = json.dumps(self.bot.RAID_DATA)

        async with self.session.post('http://devoted-gaming.shivtr.com/users/sign_in.json', headers=headers, data=data) as r:
            captured_json = await r.json()
            authenticity_token = captured_json['user_session']['authentication_token']
            return authenticity_token

    async def get_data(self, data):
        authenticity_token = await self.get_token()
        async with self.session.get('http://devoted-gaming.shivtr.com/' + data + '.json?auth_token=' + authenticity_token) as r:
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
        string_list = ', '.join(open_apps)
        number = str(len(open_apps))
        await self.bot.say('We have ' + number + ' open application(s). ' + string_list)

    @commands.command()
    async def raid(self):
        now = iso8601.parse_date(datetime.datetime.now(pytz.timezone('Europe/Amsterdam')).replace(microsecond=0).isoformat())
        events_json = await self.get_data('events')
        for i in events_json['event_objects']:
            if(iso8601.parse_date(i['date'])>now):
                raid_string = 'The next event will be ' + '\'' + i['name'] + '\'' + ' on ' + iso8601.parse_date(i['date']).strftime('%a %d %B %H:%M') + ', please visit http://devoted-gaming.shivtr.com/events/' + str(i['id']) + '?event_instance_id=' + str(i['event_category_id']) + ' to sign up!'
                break
            else:
                raid_string = 'There are currently no events scheduled.'

        await self.bot.say(raid_string)

def setup(bot):
    bot.add_cog(Raid(bot))
from discord.ext import commands
import discord
import datetime
import iso8601
import pytz
import json
import aiohttp
import re
import asyncio
import pytz

class Raid:

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.reminder = self.bot.loop.create_task(self.scheduler())

    def __unload(self):
        self.session.close()
        self.reminder.cancel()

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

    async def signup_reminder(self):
        channel = self.bot.get_channel('314866130600853516')
        reminder_message = 'Sign up window closes in 1 hour, type !raid in chat for a link to the event.'
        embed = discord.Embed(colour=0xFF9900, description=reminder_message)
        await self.bot.send_message(channel, '@everyone')
        await self.bot.send_message(channel, embed=embed)

    async def signup_close(self):
        channel = self.bot.get_channel('314866130600853516')
        closed_message = 'Sign up window has now closed. If for whatever reason you missed the window, type !raid in chat for a link to the event and comment your status.'
        embed = discord.Embed(colour=0xFF0000, description=closed_message)
        await self.bot.send_message(channel, '@everyone')
        await self.bot.send_message(channel, embed=embed)

    async def scheduler(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(5)
        while not self.bot.is_closed:
            tz = pytz.timezone('Europe/Amsterdam')
            now = datetime.datetime.now(tz)
            if datetime.datetime.today().weekday() in (1,5) and now.strftime('%H%M') == '1745':
                await self.signup_reminder()
            elif datetime.datetime.today().weekday() in (1,5) and now.strftime('%H%M') == '1845':
                await self.signup_close()
            else:
                pass
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(Raid(bot))

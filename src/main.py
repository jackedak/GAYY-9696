import json
import discord
from discord.ext import commands
import logging
import re
import time
from config import responses, bonkles
import sqlite3
import random
import os

token = os.environ['gayytoken']

logging.basicConfig(
    filename="log.txt",
    encoding="utf-8",
    filemode='a',
    format="{asctime} {levelname}:{name}:{message}",
    style='{',
    datefmt="%Y-%m-%d %H:%M",
)
logging.debug("Started bot")

all_sent = []
intents = discord.Intents.all()
intents.message_content = True
activity = discord.Activity(name='Men getting oiled up.', type=discord.ActivityType.watching)
client = discord.Client(activity=activity, intents=intents)
conn = sqlite3.connect('store.db')
cursor = conn.cursor()
bot = commands.Bot(intents=intents, command_prefix='!')


cursor.execute('''CREATE TABLE IF NOT EXISTS disabled
             (id unsigned big int, time real)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS dc
             (id unsigned big int, time real)''')



@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!enablechannel':
        if message.channel.permissions_for(message.author).manage_channels or message.author.id == 561328826123026453:
            cursor.execute(f'''DELETE FROM dc WHERE id = {message.channel.id}''')
            conn.commit()
            await message.channel.send("Enabled bot in channel. To re-disable, please run !disablechannel", reference=message)
            return
        else:
            await message.channel.send("You do not have manage channel permission, and you are not <@561328826123026453>, so no.", reference=message)
            return
    cursor.execute(f"SELECT * FROM dc WHERE id = {message.channel.id}")
    if cursor.fetchall():
        return
    if message.author.id == 935189080378056724:
        # ITS BONKLE
        for msg, func in bonkles.items():
            if msg in message.content:
                await func(message, message)
                return
        print(message.content)
    if message.content == '!enable':
        cursor.execute(f'''DELETE FROM disabled WHERE id = {message.author.id}''')
        conn.commit()
        await message.channel.send("Enabled bot for your user. To re-disable, please run !disable", reference=message)
        return
    cursor.execute(f"SELECT * FROM disabled WHERE id = {message.author.id}")
    if cursor.fetchall():
        return
    if random.randint(1, 200) == 1:
        await message.channel.send(f"I love <@1297510410689187843>")
    if message.content == '!disable':
        cursor.execute(f'''INSERT INTO disabled VALUES ({message.author.id}, {time.time()})''')
        conn.commit()
        await message.channel.send("Disabled bot for your user. To re-enable, please run !enable", reference=message)
        return
    if message.content == '!disablechannel':
        if message.channel.permissions_for(message.author).manage_channels or message.author.id == 561328826123026453:
            cursor.execute(f'''INSERT INTO dc VALUES ({message.channel.id}, {time.time()})''')
            conn.commit()
            await message.channel.send("Disabled bot in channel, to re-enable, please run !enablechannel", reference=message)
            return
        else:
            await message.channel.send("You do not have manage channel permission, and you are not <@561328826123026453>, so no.", reference=message)
            return
    if message.content.startswith('!gayysay '):
        await message.channel.send(f"{message.content[9:]}", reference=message)
        return
    if random.randint(1, 200) == 1:
        await message.channel.send(f"<@{random.choice(message.guild.members).id}> is awesome", mention_author=False)
    didex = False
    for regex, func in responses.items():
        if re.match(regex, message.content.lower()):
            await func(message, None)
            didex = True
            break
    if client.user.mentioned_in(message) and not didex and not message.reference:
        msg = await message.channel.send(random.choice([
            'Heyyyyy bestie! Whatya want? <3',
            'Im here!',
            'what does your gay ass want',
            'heyy gay',
            'hello homo',
            'homo hello',
            'wassup',
            'wazzup'
            'big poopoo'
        ]))
def main():
    client.run(token)
try:
    if __name__ == '__main__':
        main()
except:
    json.dump({"words":list(words)}, open("words.json", 'w'))

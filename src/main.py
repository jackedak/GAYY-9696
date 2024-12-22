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
from PIL import Image, ImageDraw, ImageFont

token = os.environ['gayytoken']
font = ImageFont.truetype('font.ttf', 20)

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
client = discord.Bot(activity=activity, intents=intents)
conn = sqlite3.connect('store.db')
cursor = conn.cursor()
lng = 0

cursor.execute('''CREATE TABLE IF NOT EXISTS disabled
             (id unsigned big int, time real)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS dc
             (id unsigned big int, time real)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS config
             (key varchar(12), val bigint, server unsigned big int)''')             


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
    if message.content.startswith('!config.'):
        if message.author.id == 860599288034623509:
            return
        if not (message.channel.permissions_for(message.author).administrator or message.author.id == 561328826123026453):
            await message.channel.send(f"https://i.imgflip.com/99e4an.jpg", reference=message)
            return
        parts = message.content.split()
        key = ''.join(filter(str.isalpha, parts[0].split('.')[1]))
        if len(parts) == 1:
            cursor.execute(f"SELECT * FROM config WHERE key = '{key}' AND server = '{message.guild.id}'")
            fetched = cursor.fetchall()
            if fetched:
                await message.channel.send(f"Value of \"{key}\" is {fetched[0][1]}", reference=message)
                return
            else:
                await message.channel.send(f"\"{key}\" has not been set. To set run !config.{key} [VALUE]", reference=message)
                return
        elif len(parts) == 2:
            if not message.content.split()[1].isnumeric():
                await message.channel.send(f"You can't do that dumbass. {message.content.split()[1]} is not an integer.")
                return
            value = parts[1]
            value=value.replace('\u2070','**0')
            value=value.replace('\u00B2','**2')
            value=value.replace('\u00B3','**3')
            value=value.replace('\u2074','**4')
            value=value.replace('\u2075','**5')
            value=value.replace('\u2076','**6')
            value=value.replace('\u2077','**7')
            value=value.replace('\u2078','**8')
            value=value.replace('\u2079','**9')
            value=value.replace('\u00B9','**1')
            value=eval(value)
            cursor.execute(f'''DELETE FROM config WHERE key = \'{key}\' AND server = \'{message.guild.id}\'''')
            cursor.execute(f'''INSERT INTO config VALUES ('{key}', {value}, '{message.guild.id}')''')
            conn.commit()
            await message.channel.send(f"Set {key} to {value}", reference=message)
            return
    if random.randint(1, 50) == 1:
        rv = random.randint(1,10)
        if rv == 1:
            user = random.choice(message.guild.members).id
            if user not in [712966367808192573]:
                await message.channel.send(f"<@{random.choice(message.guild.members).id}> is awesome", mention_author=False)
        else:
            await message.channel.send(random.choice([
                "Haters gonna hate, hate, hate, hate, hate.",
                "Eminem? More like femisfem.",
                "Evelyn is a gworl",
                "Homophobicus deletus",
                "Ender has bender her gender",
                "Robo will perform mitosister",
                "Habik will cause unbelievable, massive amounts of havoc",
            ]))
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
        
@client.event
async def on_reaction_add(reaction, user):
    try:
        global lng
        cursor.execute(f"SELECT * FROM config WHERE key = 'nostarself' AND server = '{reaction.message.guild.id}'")
        fetched = cursor.fetchall()
        if fetched:
            if fetched[0][1] and reaction.emoji == '⭐' and reaction.message.author.id == user.id:
                await reaction.remove(user)
                #if time.time()-lng < 10:
                #    return
                await reaction.message.channel.send("No glazing yourself, only i get to glaze u", reference=reaction.message)
                lng  = time.time()
    except Exception as e:
        print(f"{e} in server {reaction.message.guild.id} channel {reaction.message.channel.id} message {reaction.message.id}")

@client.command(description="Forge a license :3")
async def license(ctx, 
                flag: discord.Option(str, "What pride flag?",choices=["Gay", "Lesbian", "Rainbow", "Progress", "Bi", "Pan"]), 
                pronouns: discord.Option(str, "What are your pronouns?")
                ):
    global font
    assert flag in ["Gay", "Lesbian", "Rainbow", "Progress", "Bi", "Pan"]
    base = Image.open("base.png")
    flagimg = Image.open(f"{flag}.png")
    base.paste(flagimg, (0,0), flagimg)
    I1 = ImageDraw.Draw(base)
    I1.text((368, 155), ctx.author.display_name, font=font, fill=(0, 0, 0))
    I1.text((400, 190), pronouns, font=font, fill=(0, 0, 0))
    base.save('temp.png')
    with open("temp.png", "rb") as f:
        image = discord.File(f)
        await ctx.respond(file=image)
    
def main():
    client.run(token)
try:
    if __name__ == '__main__':
        main()
except:
    json.dump({"words":list(words)}, open("words.json", 'w'))
    json.dump({"words":list(words)}, open("words.json", 'w'))
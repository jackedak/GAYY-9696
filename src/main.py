'''
Copyright (C) 2025  Avalyn Baldyga
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 2 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import json
import discord
from discord.ext import commands
import logging
import re
import time
from config import responses, bonkles
import config
import sqlite3
import random
import os
from PIL import Image, ImageDraw, ImageFont
import atexit
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sentience

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
data = json.load(open('words.json', 'r'))
words = data["words"]
intents = discord.Intents.all()
intents.message_content = True
activity = discord.Activity(name='Men getting oiled up.', type=discord.ActivityType.watching)
client = discord.Bot(activity=activity, intents=intents)
conn = sqlite3.connect('store.db')
cursor = conn.cursor()
predict = client.create_group("predict", "Predict if someone might be a pretty little fruitcake :3")
try:
    model = sentience.tf.keras.models.load_model('model.keras')
except:
    model = sentience.create_model()
    print("Could not load model.")
print(model.summary())
lng = 0
lastsave = time.time()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS disabled
            (id unsigned big int, time real)
''')
cursor.execute('''
            CREATE TABLE IF NOT EXISTS dc
            (id unsigned big int, time real)
''')
cursor.execute('''
            CREATE TABLE IF NOT EXISTS config
            (key varchar(12) NOT NULL, val bigint, server unsigned big int NOT NULL)
''') 
cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications 
            (name varchar(16) NOT NULL UNIQUE, userid unsigned big int NOT NULL, time real, condition varchar(64) NOT NULL)
''')
cursor.execute('''
            CREATE TABLE IF NOT EXISTS noai
            (userid unsigned big int NOT NULL UNIQUE)
''')
cursor.execute('''
            CREATE TABLE IF NOT EXISTS falling
            (userid unsigned big int NOT NULL UNIQUE)
''')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global lastsave
    if message.author == client.user:
        return
    if not message.guild.id in [1305760193191346186, 1290860835266363452, 1299171183463235604]:
        print(f"{message.guild.name} {message.content}: {message.author.id} {message.author.display_name}")
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
    if message.content == '!enable':
        cursor.execute(f'''DELETE FROM disabled WHERE id = {message.author.id}''')
        conn.commit()
        await message.channel.send("Enabled bot for your user. To re-disable, please run !disable", reference=message)
        return
    cursor.execute(f"SELECT * FROM disabled WHERE id = {message.author.id}")
    if cursor.fetchall():
        return

    result = cursor.execute(f"SELECT * FROM notifications WHERE userid = {message.author.id}")
    for (name, userid, ctime, condition) in result.fetchall():
        try:
            if (eval(condition, {
                "content": message.content,
                "sender": message.author.id,
                "server": message.guild.id,
                "channel": message.channel.id,
                "time": time.time(),
                "notifname": name,
                "authorusername": message.author.name,
                "re": re
            }, {})):
                await client.get_user(userid).send(f"Your notification, ```{name}```, triggered! [Jump to message]({message.jump_url})")
        except Exception as e:
            await client.get_user(userid).send(f"Your notification, ```{name}```, failed with exception {e} and has been automatically deleted")
            cursor.execute(f'''DELETE FROM notifications WHERE userid = (?) AND name = (?)''', (userid, name))
    conn.commit()
    if random.randint(1, 200) == 1:
        await message.channel.send(f"I love <@1297510410689187843>")
    if message.content == '!disable':
        cursor.execute(f'''INSERT INTO disabled VALUES ({message.author.id}, {time.time()})''')
        conn.commit()
        await message.channel.send("Disabled bot for your user. To re-enable, please run !enable", reference=message)
        return
    if message.content == '!noai':
        cursor.execute(f'''INSERT INTO noai VALUES ({message.author.id})''')
        conn.commit()
        await message.channel.send("Disabled AI training from your messages. To re-enable, please run !yesai", reference=message)
        return
    if message.content == '!yesai':
        cursor.execute(f'''DELETE FROM noai WHERE userid = {message.author.id}''')
        conn.commit()
        await message.channel.send("Enabled AI training from your messages. To re-disable, please run !noai", reference=message)
        return
    if message.content == '!norsp':
        cursor.execute(f'''INSERT INTO falling VALUES ({message.author.id})''')
        conn.commit()
        await message.channel.send("Disabled responses to your messages. To re-enable, please run !respond", reference=message)
        return
    if message.content == '!respond':
        cursor.execute(f'''DELETE FROM falling WHERE userid = {message.author.id}''')
        conn.commit()
        await message.channel.send("Enabled responses to your messages. To re-disable, please run !norsp", reference=message)
        return

    cursor.execute(f"SELECT * FROM falling WHERE userid = {message.author.id}")
    srsp = not cursor.fetchall()
    if srsp:
        # ITS BONKLE OR SKAMTEBORD
        for msg, func in bonkles.items():
            if msg in message.content:
                await func(message, message)


    cursor.execute(f"SELECT * FROM noai WHERE userid = {message.author.id}")
    if not cursor.fetchall():
        messageref = message.reference
        if messageref:
            try:
                sentience.train(model, messageref.resolved.content, message.content)
            except:
                pass
    if random.randint(1,40) == 5 and srsp:
        prediction = sentience.predict(model, message.content)
        print(prediction)
        await message.channel.send(prediction, reference=message)
    if time.time() - lastsave > 60:
        model.save('model.keras')
        lastsave = time.time()

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
        await message.channel.send(f"{message.content[9:]}")
        try:
            await message.delete()
        except:
            pass
        return

    if message.content.startswith('!notify '):
        name = message.content.split(' ')[1]
        condition = ' '.join(message.content[8:].split(' ')[1:])
        if name == "delete":
            if condition == '*':
                cursor.execute(f'''DELETE FROM notifications WHERE userid = (?)''', (message.author.id,))
            else:
                cursor.execute(f'''DELETE FROM notifications WHERE userid = (?) AND name = (?)''', (message.author.id, condition))
            conn.commit()
            return
        if not condition:
            await message.channel.send("""Command syntax: ```!notify [name] [condition]```to add a notification. [condition] must be a valid python expression, where "content" is the text of the message, "sender" is the user ID of the message author, "server" is the ID of the server where the message was send, "channel" is the ID of the channel where the message was sent, "notifname" is the previously entered name of this notification, and authorusername is the username of the message author. The python RegEx library is available under "re". To delete this notification, do !notify delete [name]. To delete all notifications, do !notify delete *""", reference=message
            )
            return
        for word in config.banned_words:
            if word in condition:
                await message.channel.send(f"Condition may not contain '{word}' for security reasons.", reference=message)
                return
        cursor.execute(f'''INSERT INTO notifications VALUES ((?), (?), (?), (?))''', (name, message.author.id, time.time(), condition))
        conn.commit()
        await message.channel.send("Notification successfully created.", reference=message)

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

    if random.randint(1, 50) == 1 and srsp:
        rv = random.randint(1,10)
        if rv == 1:
            user = random.choice(message.guild.members).id
            if user not in [712966367808192573,1297510410689187843]:
                await message.channel.send(f"<@{random.choice(message.guild.members).id}> is awesome", silent=True)
            if user == 1297510410689187843:
                await message.channel.send(f"<@{random.choice(message.guild.members).id}> are awesome", mention_author=False)
        else:
            await message.channel.send(random.choice([
                "Haters gonna hate, hate, hate, hate, hate.",
                "Eminem? More like femisfem.",
                "Evelyn is a gworl",
                "Homophobicus deletus",
                "Ender has bender her gender",
                "Tina will perform mitosister",
                "Habik will cause unbelievable, massive amounts of havoc",
            ]))

    didex = False
    for regex, func in responses.items():
        if re.match(regex, message.content.lower()):
            await func(message, None)
            didex = True
            break
    wordss = message.content.lower()
    wordss = filter(lambda x: x.isalpha() or x.isspace(), wordss)
    wordss = ''.join(wordss).split()
    #for word in wordss:
    #    if not word in words:
    #        words.append(word)
    #sentience.words = words
    if client.user.mentioned_in(message) and not didex and not message.reference:
        if message.author.id == 936030536021999637:
            await message.channel.send("You are such an egg.", reference=message)
            return
        if srsp:
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
    json.dump({"words": words}, open('words.json', 'w'))
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
                flag: discord.Option(str, "What pride flag?",choices=["Gay", "Lesbian", "Rainbow", "Progress", "Bi", "Pan", "Arizona", "Trans"]), 
                pronouns: discord.Option(str, "What are your pronouns?")
                ):
    global font
    assert flag in ["Gay", "Lesbian", "Rainbow", "Progress", "Bi", "Pan", "Arizona", "Trans"]
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

@predict.command(description="Predict whether or not someone is totally an egg or not :3")
async def egg(ctx, user: discord.Option(discord.SlashCommandOptionType.user , "What user?")):
    rng = random.randint(1,100)
    if user.id == 936030536021999637:
        rng += 100
    if random.randint(1,10) == 1:
        rng*=user.id
    embed = discord.Embed(
        title=f"{rng}%",
        description=f"<@{user.id}> is {rng}% an egg.",
        color=discord.Colour.blurple(),
    )
    await ctx.respond("", embed=embed)

def grace():
    json.dump({"words": words}, open('words.json', 'w'))
    print("shutdown bot")
atexit.register(grace)
try:
    if __name__ == '__main__':
        client.run(token)
except:
    json.dump({"words": words}, open('words.json', 'w'))
    model.save('model.keras')
    print("shutdown bot")

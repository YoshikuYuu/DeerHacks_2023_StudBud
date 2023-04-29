'''A collection of functions that interact with the sqlite3 database.'''
import discord
import random
from discord.ext import commands
import sqlite3
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

# make database with user, task, and time
# store time as datetime object if possible?
# id is datetime.datetime.now
# connecting to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY NOT NULL,
                    task TEXT,
                    time DATETIME,
                    complete BOOL,
                    incomplete BOOL)''')
# # prints database
# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()

# for row in rows:
#     print(row)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

    # checking if they're already in db
    username = message.author.name
    discriminator = message.author.discriminator
    user_id = f"{username}#{discriminator}"
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    # if they're not in db add them
    if not result:
        username = message.author.name
        discriminator = message.author.discriminator
        user_id = f"{username}#{discriminator}"
        cursor.execute("INSERT INTO users (user_id, task) VALUES (?, '')", (user_id,))
        conn.commit()

    # close database connection
    cursor.close()
    conn.close()

    encouraging_quotes = [
        'Keep going, you can do it!', 'I believe in you!',
        "You're doing awesome!"
    ]

    if 'encourag' in message.content.lower():
        response = random.choice(encouraging_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

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


# bot event that initializes user in database if the user isn't already in the database
# user is initialized with their name, an empty string as a task, and None as time
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

# bot command to record tasks; current format example -> !task "do laundry" 7:02
# note that multiple tasks are stored in JSON format
# bug in code about time storage that i'm currently fixing - alisha
@bot.command(name='task')
async def record_task(ctx, task: str, time_str: str):
    try:
        # remember to convert time_str into the appropriate format
        time = datetime.strptime(str(time_str), '%I:%M')
        time_formatted = time.strftime('%H:%M')
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        user_id = f"{username}#{discriminator}"

        cursor.execute("SELECT task FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        if result is not None and result != '':
            try:
                current_tasks = json.loads(result[0])
            except json.JSONDecodeError:
                current_tasks = []
        else:
            current_tasks = []
        current_tasks.append({"task": task, "time": time_formatted})
        cursor.execute("REPLACE INTO users (user_id, task) VALUES (?, ?)", (user_id, json.dumps(current_tasks)))
        conn.commit()

        await ctx.send(f'Recorded task {task}. Reminder set for {time_formatted}.')
    except ValueError as e:
        await ctx.send(f'Error {e}. Invalid time format. Please use the format "HH:MM AM/PM".')
    except json.JSONDecodeError as e:
        print(f'Error {e}. JSON string: {result[0]}')
        await ctx.send(f'Error {e}. Failed to load tasks from database.')

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

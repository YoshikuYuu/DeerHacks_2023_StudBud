'''A collection of functions for StudBud that alter the database.'''
import discord
import random
from discord.ext import commands
import sqlite3
from datetime import datetime
import json

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
                    tasks TEXT DEFAULT '{}',
                    complete BOOL,
                    incomplete BOOL)''')
# # prints database
# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

# initializes database with user if the user is new and sends message
# note that this doesn't correctly handle the case where the first message is a !task command
# TODO: fix issue outlined in above comment
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
        cursor.execute("INSERT INTO users (user_id, tasks) VALUES (?, '')", (user_id,))
        conn.commit()

    encouraging_quotes = [
        'Keep going, you can do it!', 'I believe in you!',
        "You're doing awesome!"
    ]

    if 'encourag' in message.content.lower():
        response = random.choice(encouraging_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

# records a task in the database
# sample format for task command -> !task "study for math test" 11:00
# TODO: correctly handle time objects in order to search for time and ping when required
# sample database row when two tasks are stored looks like this:
# ('thepandabear123#4256', '{"do laundry": "06:00", "study for math test": "11:00"}', None, None)
# TODO: handle cases where the task is complete/incomplete (how do we keep track?)
@bot.command(name='task')
async def record_task(ctx, task: str, time_str: str):
    try:
        # remember to convert time_str into the appropriate format
        time = datetime.strptime(str(time_str), '%I:%M')
        time_formatted = time.strftime('%H:%M')
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        user_id = f"{username}#{discriminator}"

        cursor.execute("SELECT tasks FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        if result is not None and result != '':
            try:
                current_tasks = json.loads(result[0])
            except json.JSONDecodeError:
                current_tasks = {}
        else:
            current_tasks = {}

        current_tasks[task] = time_formatted
        cursor.execute("UPDATE users SET tasks=? WHERE user_id=?", (json.dumps(current_tasks), user_id))
        conn.commit()

        await ctx.send(f'Recorded task {task}. Reminder set for {time_formatted}.')
    except ValueError as e:
        await ctx.send(f'Error {e}. Invalid time format. Please use the format "HH:MM AM/PM".')
    except json.JSONDecodeError as e:
        print(f'Error {e}. JSON string: {result[0]}')
        await ctx.send(f'Error {e}. Failed to load tasks from database.')

# closing the database is currently causing an issue; need to look into it so i've commented it out for now
# shouldn't cause any issues because the database is currently stored locally on my laptop
# # close database connection
# cursor.close()
# conn.close()

bot.run(
    'MTEwMTYzODEwNTg1OTEwNDc2OA.GEWumY.Q4rY9e0zlpF-mUqWvJj4ODIyT93JZ4gZs8MZgY')

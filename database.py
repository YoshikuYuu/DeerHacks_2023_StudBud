#ALL OF THIS HAS BEEN INTEGRATED INTO BOT.PY



'''A collection of functions that interact with the sqlite3 database.'''
import discord
import random
from discord.ext import commands
import sqlite3
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

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

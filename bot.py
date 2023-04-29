import discord
from reminder import *
from datetime import datetime, timezone
from discord.ext import commands, tasks
import sqlite3
import json
import random

def run_discord_bot():
    ###
    TOKEN = 'MTEwMTMyNDY0MDg5MjI0NDAzMA.GpOKLH.1-G0Gu-hs9wgUPHKTpxbcDJyeXn3kDW9CC2xI0'

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    # Following code makes a database with user, task, and time
        # Store time as datetime object if possible?
        # id is datetime.datetime.now
    # Connecting to the database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY NOT NULL,
                    task TEXT,
                    time DATETIME,
                    complete BOOL,
                    incomplete BOOL)''')
    ###

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')

    @bot.command(name="hi")
    async def hi(ctx):
        await ctx.send(f'Hi, {ctx.author.mention}')


    @bot.command(name="register")
    async def register(ctx):
        # checking if they're already in db
        username = ctx.author.name
        discriminator = ctx.author.discriminator
        user_id = f"{username}#{discriminator}"
        cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()

        # if they're not in db add them
        if not result:
            username = ctx.author.name
            discriminator = ctx.author.discriminator
            user_id = f"{username}#{discriminator}"
            cursor.execute("INSERT INTO users (user_id, task) VALUES (?, '')", (user_id,))
            conn.commit()

        # close database connection
        # cursor.close()
        # conn.close()

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


    @tasks.loop(minutes=1)
    async def check_time():
        # Unimplmented: Get list of datetime objects from db
        reminders = get_reminders()
        current_datetime = datetime.now(timezone.utc)

        if current_datetime in reminders:
            # Unimplemented: Get reminder details from db and send ping/dm
            send_reminders(current_datetime, bot)

    @check_time.before_loop
    # Waits for the bot to start up before beginning the check_time loop
    async def before_check_time():
        await bot.wait_until_ready()



    bot.run(TOKEN)

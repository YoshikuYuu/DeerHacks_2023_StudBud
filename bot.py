import discord
from reminder import *
from datetime import datetime, timezone
from discord.ext import commands, tasks
import sqlite3
import random

def run_discord_bot():
    ###
    TOKEN = 'MTEwMTMyNDY0MDg5MjI0NDAzMA.GpOKLH.1-G0Gu-hs9wgUPHKTpxbcDJyeXn3kDW9CC2xI0'

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    ###

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

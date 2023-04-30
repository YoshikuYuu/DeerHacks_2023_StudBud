import discord
from reminder import *
from db import *
from datetime import datetime, timezone
from discord.ext import commands, tasks

def run_discord_bot():

    ###
    TOKEN = 'MTEwMTMyNDY0MDg5MjI0NDAzMA.GpOKLH.1-G0Gu-hs9wgUPHKTpxbcDJyeXn3kDW9CC2xI0'

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='$', intents=intents)

    # Initialize database and sets conn and cursor
    conn, cursor = initialize_db()

    ###

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')

        check_time.start()

    @bot.command(name="hi")
    async def hi(ctx):
        await ctx.send(f'Hi, {ctx.author.mention}')


    @bot.command(name='task')
    async def record_task(ctx, task: str, time_str: str):
        user_id = f"{ctx.author.name}#{ctx.author.discriminator}"
        if not user_in_db(cursor, user_id):
            add_user_to_db(cursor, conn, user_id)
        try:
            # remember to convert time_str into the appropriate format
            time = datetime.strptime(str(time_str), '%H:%M')
            time_formatted = time.strftime('%H:%M')

            add_task(cursor, conn, user_id, task, time_formatted)

            await ctx.send(f'Recorded task: "{task}". Reminder set for {time_formatted}.')

        except ValueError as e:
            await ctx.send(f'Error {e}. Invalid time format. Please use the format "HH:MM AM/PM".')

    @tasks.loop(minutes=1)
    async def check_time():
        # Unimplmented: Get list of datetime objects from db
        reminders = get_reminders(cursor)
        current_datetime = datetime.now(timezone.utc)
        print(current_datetime)

        if current_datetime in reminders:
            # Unimplemented: Get reminder details from db and send ping/dm
            send_reminders(cursor, current_datetime, bot)

    @check_time.before_loop
    # Waits for the bot to start up before beginning the check_time loop
    async def before_check_time():
        await bot.wait_until_ready()
        print("Starting loop.")




    bot.run(TOKEN)

import discord
from reminder import *
from db import *
from datetime import datetime
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
        user_id = str(ctx.author.id)
        if not user_in_db(cursor, user_id):
            add_user_to_db(cursor, conn, user_id)
        try:
            # remember to convert time_str into the appropriate format
            p_time_str = datetime.strptime(time_str, '%H:%M')
            task_time = datetime.now()
            task_time = task_time.replace(hour=p_time_str.hour,
                                          minute=p_time_str.minute)
            f_task_time = task_time.strftime('%d/%m/%y %H:%M')
            print(f_task_time)

            add_task(cursor, conn, user_id, task, f_task_time)

            await ctx.send(f'Recorded task: "{task}". Reminder set for {f_task_time}.')

        except ValueError as e:
            await ctx.send(f'Error {e}. Invalid time format. Please use the format "HH:MM".')


    @bot.command(name='done')
    async def done_task(ctx, finished_task: str):
        tasks_dict = get_user_tasks(cursor, ctx.author.id)
        for task in tasks_dict:
            if finished_task == task:
                add_points(cursor, 50, ctx.author.id)
                await ctx.send("Good job on completing that task! You've earned 50 points!")


    @tasks.loop(minutes=1)
    async def check_time():
        # Unimplmented: Get list of datetime objects from db
        reminders = get_reminders(cursor)
        current_datetime = datetime.now().strftime('%d/%m/%y %H:%M')
        print(current_datetime)
        print(reminders)

        if current_datetime in reminders:
            # Unimplemented: Get reminder details from db and send ping/dm
            task_tups = send_reminders(cursor, current_datetime, bot)

            for task in task_tups:
                user = await bot.fetch_user(int(task[0]))  # Need to test if this works
                await user.send(f"Reminder to complete task: {task[1]}")

    @check_time.before_loop
    # Waits for the bot to start up before beginning the check_time loop
    async def before_check_time():
        await bot.wait_until_ready()
        print("Starting loop.")


    bot.run(TOKEN)

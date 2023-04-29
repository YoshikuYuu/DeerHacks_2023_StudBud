import discord
from reminder import *
from datetime import datetime, timezone
from discord.ext import commands, tasks

def run_discord_bot():
    ###
    TOKEN = 'MTEwMTMyNDY0MDg5MjI0NDAzMA.GpOKLH.1-G0Gu-hs9wgUPHKTpxbcDJyeXn3kDW9CC2xI0'

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    ###

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')

    @bot.command(name="hi")
    async def hi(ctx):
        await ctx.send(f'Hi, {ctx.author.mention}')


    @tasks.loop(minutes=1)
    async def check_time():
        # Unimplmeneted: Get list of datetime objects from db
        reminders = get_reminders()
        current_datetime = datetime.now(timezone.utc)

        if current_datetime in reminders:
            # Unimplemented: Get reminder details from db and send ping/dm
            send_reminders(current_datetime)


    @check_time.before_loop
    # Waits for the bot to start up before beginning the check_time loop
    async def before_check_time():
        await bot.wait_until_ready()

    bot.run(TOKEN)

from __future__ import annotations
from datetime import datetime
from discord.ext import commands


def get_reminders():
    pass


def send_reminders(time: datetime, bot):
    """
    Gets all tasks that correspond to the given time and sends reminders for
    the tasks.

    :param time: datetime object storing a reminder time
    :param bot: discord bot
    :return: None
    """

    # Unimplemented: function to get a list of tuples (u_id, task_name) from db
    # that have a task that corresponds to time
    tasks = db_get_tasks(time)

    for task in tasks:
        user = bot.get_user(task[0])  # Need to test if this works
        user.send(f"Reminder: {task[1]}")

def db_get_tasks():
    pass

from __future__ import annotations
from datetime import datetime
from discord.ext import commands
from bot import *
from database import *


def _get_reminders_helper(times):
    """Given a list of strings that represent the times a task are due,
    convert each string into a datetime object and return the list of
    datetime objects."""
    new_times = []
    for time in times:
        new_times.append(datetime.strptime(time, '%H:%M'))
    return new_times


def get_reminders():
    cursor.execute("SELECT user_id, tasks FROM users")
    values = cursor.fetchall()
    reminders = []
    for value in values:
        tasks_str = value[1]
        tasks_dict = json.loads(tasks_str)
        times = [time_str for time_str in tasks_dict]
        reminders.extend(_get_reminders_helper(times))
    return reminders


def db_get_tasks(time):
    cursor.execute("SELECT user_id, tasks FROM users")
    values = cursor.fetchall()
    matching_tasks = []
    for value in values:
        user_id = value[0]
        tasks = json.loads(row[1])
        for task, time_str in tasks.items():
            # converting time_str into datetime object to compare to
            # datetime.datetime.now()
            task_time = datetime.strptime(time_str, '%H:%M')
            if task_time == time:
                matching_tasks.append((user_id, task))
    return matching_tasks


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

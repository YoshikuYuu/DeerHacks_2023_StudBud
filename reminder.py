from __future__ import annotations
from datetime import datetime
from discord.ext import commands
from db import *
from bot import *
import json


def _get_reminders_helper(times):
    """Given a list of strings that represent the times a task are due,
    convert each string into a datetime object and return the list of
    datetime objects."""
    new_times = []
    # for time in times:
    #     new_times.append(datetime.strptime(time, '%d/%m/%y %H:%M'))
    for time in times:
        new_times.append(time)
    return new_times


def get_reminders(cursor):
    cursor.execute("SELECT user_id, tasks FROM users")
    user_task_tups = cursor.fetchall()
    reminders = []
    for tup in user_task_tups:
        tasks_str = tup[1]
        if tasks_str != '':
            tasks_dict = json.loads(tasks_str)
            times = [tasks_dict[task] for task in tasks_dict]
            reminders.extend(_get_reminders_helper(times))
    return reminders


def send_reminders(cursor, time: str, bot) -> list:
    """
    Gets all tasks that correspond to the given time and sends reminders for
    the tasks.
    """

    # Unimplemented: function to get a list of tuples (u_id, task_name) from db
    # that have a task that corresponds to time
    task_tups = db_get_tasks_time(cursor, time)
    return task_tups



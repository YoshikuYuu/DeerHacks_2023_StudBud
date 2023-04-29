from __future__ import annotations
from datetime import datetime
from bot import bot


def get_reminders():
    pass

def send_reminders(time: datetime):
    # Unimplemented: function to get all user ids from db that have a task that
    # corresponds to time
    user_ids = db_get_user_ids(time)

    for id in user_ids:
        user = bot.get_user(id)  # Need to test if this works
        await user.send("Reminder message.")



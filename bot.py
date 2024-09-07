from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import pytz
import os

# Get the token and chat_id from environment variables (Heroku best practice)
bot_token = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CHAT_ID')
message_thread_id = int(os.environ.get('MESSAGE_THREAD_ID'))  # Default to 3 if not set

# Create the bot instance
bot = Bot(token=bot_token)

# Define the timezone for Zurich
zurich_timezone = pytz.timezone('Europe/Zurich')

# Define the message you want to send
announcement_text = """📅 Bitte eintragen: BR Zeitplan für nächste Woche 📅

MO: Manic Pixxxies (Abend)
DI: Corokia (17-19h), Jam (Abend)
MI: Dylan (Tagsüber), Zahfee (Abend)
DO: Rapid Anti (Abend)
FR: Saltwater Sirens (Abend)
SA:
SO: Pferd (Abend)

Wenn ihr euren Slot nicht braucht, Nachricht kopieren, euch rausnehmen und wieder in den Chat schicken. Wenn ihr einen freien Slot reservieren wollt, Nachricht kopieren, eintragen, wieder in den Chat schicken. Bitte auch bei spontanen Änderungen! 💕"""

# Function to send the message
async def send_message_async():
    await bot.send_message(chat_id=chat_id, text=announcement_text, message_thread_id=message_thread_id)

def send_scheduled_message():
    asyncio.run(send_message_async())

# Initialize the scheduler
scheduler = BlockingScheduler(timezone=zurich_timezone)

# Schedule the message every Saturday at 15:30 PM Zurich time
scheduler.add_job(send_scheduled_message, CronTrigger(day_of_week='sat', hour=15, minute=30))

# Start the scheduler
scheduler.start()
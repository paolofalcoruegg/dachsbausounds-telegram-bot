import os
import logging
import asyncio
from flask import Flask
from telegram import Bot
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Replace these with your actual credentials
bot_token = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CHAT_ID')
message_thread_id = int(os.environ.get('MESSAGE_THREAD_ID'))

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

# Async function to send the scheduled message
async def send_message_async():
    await bot.send_message(chat_id=chat_id, text=announcement_text, message_thread_id=message_thread_id)
    logger.info("Sent scheduled message.")

# Function to schedule the async message sending
def send_scheduled_message():
    logger.info("Attempting to send scheduled message..")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_message_async())
    loop.close()

# Initialize the scheduler
scheduler = BackgroundScheduler(timezone=zurich_timezone)

# Schedule the message every Saturday at 2 PM Zurich time
scheduler.add_job(send_scheduled_message, CronTrigger(day_of_week='sat', hour=14, minute=0))

# Start the scheduler
scheduler.start()

@app.route('/')
def index():
    jobs = scheduler.get_jobs()
    # Convert the jobs list to a string
    job_list = ', '.join([str(job) for job in jobs])  # Create a comma-separated string of job representations
    return f"Telegram bot is running! Scheduler Jobs: {job_list}"

if __name__ == "__main__":
    # Start the Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
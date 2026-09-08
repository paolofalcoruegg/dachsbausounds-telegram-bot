"""Send the weekly Bandraum schedule reminder to the Telegram group.

Runs once and exits. The weekly scheduling is handled by GitHub Actions,
see .github/workflows/weekly.yml.
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from telegram import Bot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

zurich_timezone = ZoneInfo('Europe/Zurich')

# Get the formatted dates of next Monday and Sunday
today = datetime.now(zurich_timezone).date()  # Get today's date
next_monday = today + timedelta(days=-today.weekday(), weeks=1)  # Calculate the date of next Monday
next_sunday = next_monday + timedelta(days=6)  # Calculate the date of next Sunday
# Format the dates as day.month.year
formatted_monday = next_monday.strftime('%d.%m.%Y')
formatted_sunday = next_sunday.strftime('%d.%m.%Y')

# Define the message you want to send
announcement_text = f"""📅 Bitte eintragen: BR Zeitplan für nächste Woche, Montag {formatted_monday} bis Sonntag {formatted_sunday}📅

MO: Saltwater Sirens (Abend)
DI: Corokia (17-19h), Jam (Abend)
MI: Dylan (14-17h), Zahfee (ab 18h)
DO: Rapid Anti (ab 18h)
FR: 
SA: 
SO: Pferd (Abend)

Wenn ihr euren Slot nicht braucht, Nachricht kopieren, euch rausnehmen und wieder in den Chat schicken. Wenn ihr einen freien Slot reservieren wollt, Nachricht kopieren, eintragen, wieder in den Chat schicken. Bitte auch bei spontanen Änderungen! 💕"""


async def send_message_async():
    bot = Bot(token=os.environ['BOT_TOKEN'])
    thread_id = os.environ.get('MESSAGE_THREAD_ID')
    async with bot:
        await bot.send_message(
            chat_id=os.environ['CHAT_ID'],
            text=announcement_text,
            message_thread_id=int(thread_id) if thread_id else None,
        )


if __name__ == '__main__':
    if '--dry-run' in sys.argv:
        print(announcement_text)
        sys.exit(0)

    logging.info(f"Sending schedule for {formatted_monday} - {formatted_sunday}...")
    try:
        asyncio.run(send_message_async())
    except Exception as e:
        # Exit non-zero so the GitHub Actions run shows up as failed and notifies.
        logging.error(f"Failed to send message: {e}")
        sys.exit(1)
    logging.info("Message sent successfully.")

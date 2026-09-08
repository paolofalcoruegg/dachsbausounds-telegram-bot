# dachsbausounds-telegram-bot

Posts the weekly Bandraum schedule reminder into the Telegram group every
Saturday afternoon.

`bot.py` sends one message and exits. The weekly trigger is a GitHub Actions
cron job in `.github/workflows/weekly.yml` — there is no server to keep running.

## Setup

Set these under **Settings → Secrets and variables → Actions**:

| Secret | Value |
| --- | --- |
| `BOT_TOKEN` | Bot token from @BotFather |
| `CHAT_ID` | ID of the group |
| `MESSAGE_THREAD_ID` | ID of the forum topic (optional — omit to post in the main chat) |

## Testing

Preview the message without sending it:

```sh
pip install -r requirements.txt
python bot.py --dry-run
```

To send for real, go to **Actions → Weekly schedule reminder → Run workflow**.

## Notes

- The cron runs at 12:15 UTC, which is 14:15 in Zurich in summer and 13:15 in
  winter. GitHub's scheduler is best-effort and can fire 10+ minutes late.
- GitHub disables scheduled workflows on public repos after 60 days without
  commits. You get a warning email; one click re-enables it.

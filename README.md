# Discord Log Handler

## Overview
`discord-log-handler` is a Python library providing a custom logging handler for dispatching log messages to Discord channels. 
You can send logs via a Discord bot or a webhook, offering flexibility for integrating Discord as a logging endpoint.

### Features
- Dispatch logs to Discord channels using either a bot or a webhook url.
- No need to install discord.py if you are using a webhook url.

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/RobertoScifo/discord-log-handler
```

## Usage

### Example: Sending Logs Using a Webhook

```python
import logging
from discord_log_handler import DiscordLogHandler

# Configure logger
logger = logging.getLogger('example')
webhook_url = 'https://discord.com/api/webhooks/...'
handler = DiscordLogHandler.from_webhook(webhook_url)
logger.addHandler(handler)

logger.error('This is a test error message!')
```

### Example: Sending Logs Using a Bot

```python
from discord.ext import commands
from discord_log_handler import configure_logging

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    configure_logging('bot_logger', bot=bot, channel_id=123456789012345678)
    logger.info('Bot is ready!')

bot.run('your-bot-token')
```


# Loggord (Discord Log Handler)

## Overview
`loggord` is a Python library providing a custom logging handler for dispatching log messages to Discord channels. 

### Features
- Dispatch logs to Discord channels using either a bot or a webhook url.
- No need to install discord.py if you are using a webhook url.

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/RobertoScifo/loggord
```

## Usage

### Sending Logs Using a Webhook

```python
import logging
from loggord import DiscordLogHandler

# Configure logger
logger = logging.getLogger('example')
webhook_url = 'https://discord.com/api/webhooks/...'
handler = DiscordLogHandler.from_webhook(webhook_url)
logger.addHandler(handler)

logger.error('This is a test error message!')
```

### Sending Logs Using a Bot

```python
from discord.ext import commands
from loggord import configure_discord_logging

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    configure_discord_logging(
        name='bot_logger',
        bot=bot,
        channel_id=123456789012345678
    )
    logger.info('Bot is ready!')

bot.run('your-bot-token')
```


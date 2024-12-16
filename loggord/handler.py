from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any
from urllib import request


if TYPE_CHECKING:
    import discord
    from discord.ext import commands


class DiscordLogHandler(logging.Handler):
    """Custom handler for dispatching logging events to a Discord channel."""

    __slots__ = ('bot', 'channel_id', '_webhook_url')

    @classmethod
    def from_bot(
        cls,
        bot: commands.Bot,
        channel_id: int
    ) -> DiscordLogHandler:
        """Create a new instance of DiscordLogHandler, using a bot."""
        return cls(bot=bot, channel_id=channel_id)
    
    @classmethod
    def from_webhook(
        cls,
        webhook_url: str
    ) -> DiscordLogHandler:
        """Create a new instance of DiscordLogHandler, using a webhook."""
        return cls(webhook_url=webhook_url)

    def __init__(
            self,
            webhook_url: str | None = None,
            bot: commands.Bot | None = None,
            channel_id: int | None = None,
    ) -> None:
        """Custom handler for dispatching logging events to a Discord channel.
    
        Parameters
        ----------
        webhook_url : `str`
            The URL of the Discord webhook to send logs to.
        bot : `commands.Bot`
            The Discord bot instance.
        channel_id : `int`
            The ID of the Discord channel to send logs to.
    
        Raises
        ------
        ValueError
            If both `bot` and `webhook_url` are provided.
        """
        if not bot and not webhook_url:
            raise ValueError('Either bot or webhook_url must be provided.')
        
        if bot and webhook_url:
            raise ValueError('Cannot provide both bot and webhook_url.')

        super().__init__()
        self.webhook_url = webhook_url
        self.bot = bot
        self.channel_id = channel_id

    def emit(self, record: logging.LogRecord) -> None:
        """Send a log record to the designated Discord channel."""
        if self.bot:
            embed = bot_format(record)
            self.bot.loop.create_task(self._send_log(embed))
        elif self.webhook_url:            
            data = json.dumps(webhook_format(record)).encode()
            req = request.Request(
                url=self.webhook_url,
                method='POST',
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0'
                },  
                data=data
            )
            with request.urlopen(req) as res:
                return


    async def _send_log(self, embed: discord.Embed) -> None:
        if self.bot:
            channel = self.bot.get_channel(self.channel_id)
            await channel.send(embed=embed)


def configure_discord_logging(
        name: str,
        bot: commands.Bot | None = None,
        channel_id: int | None = None,
        webhook_url: str | None = None
) -> logging.Logger:
    """
    Retrieve the logger and add a handler for sending records
    to the specified Discord channel. 

    Parameters
    ----------
    name : `str`
        The name of the logger.
    webhook_url : `str`
        The URL of the Discord webhook to send logs to.
    bot : `commands.Bot`
        The Discord bot instance.
    channel_id : `int`
        The ID of the Discord channel where logs are sent.

    Returns
    -------
    `logging.Logger`
        A logger with the added ability to dispatch logging events
        to a Discord channel. 

    Raises
    ------
    `ValueError`
        If both `bot` and `webhook_url` are provided.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    discord_handler = DiscordLogHandler(webhook_url, bot, channel_id)
    discord_handler.setLevel(logging.INFO)
    logger.addHandler(discord_handler)

    return logger


def bot_format(record: logging.LogRecord) -> discord.Embed:
    """Format a log record as a Discord embed."""
    import discord

    color = discord.Color(get_color(record))
    timestamp = get_timestamp(record)

    log_embed = discord.Embed(
        description=record.message,
        color=color,
        timestamp=datetime.fromisoformat(timestamp)
    )
    log_embed.add_field(name='Level', value=record.levelname)
    log_embed.add_field(name='Module', value=record.module)
    log_embed.add_field(name='Timestamp', value=timestamp)
        
    return log_embed


def webhook_format(record: logging.LogRecord) -> dict[str, Any]:
    """Format a log record as a Discord webhook payload."""
    color = get_color(record)
    timestamp = get_timestamp(record)

    return {
        'embeds': [
            {
                'description': record.message,
                'color': color,
                'timestamp': f'{timestamp.replace(" ", "T")}.000Z',
                'fields': [
                    {
                        'name': 'Level',
                        'value': record.levelname,
                        'inline': True
                    },
                    {
                        'name': 'Module',
                        'value': record.module,
                        'inline': True
                    }
                ]
            }
        ]
    }


def get_color(record: logging.LogRecord) -> int:
    if record.levelno >= 40:
        return 0xE74C3C
    elif record.levelno == 30:
        return 0xF1C40F
    else:
        return 0x95A5A6
    
    
def get_timestamp(record: logging.LogRecord) -> str:
    return record.asctime.split(',')[0]


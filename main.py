import logging
from datetime import datetime

import discord
from discord.ext import commands


class DiscordLogHandler(logging.Handler):
    """Custom handler for dispatching logging events to a Discord channel.
    
    Attributes
    ----------
    bot : commands.Bot
        The Discord bot instance.
    channel_id : int
        The ID of the Discord channel where logs are sent.
    """
    def __init__(
            self, 
            bot: commands.Bot, 
            channel_id: int
    ) -> None:
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id

    def emit(self, record: logging.LogRecord) -> None:
        """Send a log record to the designated Discord channel."""
        log_embed = self.format(record)
        self.bot.loop.create_task(self._send_log(log_embed))

    async def _send_log(self, embed: discord.Embed) -> None:
        channel = self.bot.get_channel(self.channel_id)
        await channel.send(embed=embed)

    def format(self, record: logging.LogRecord) -> discord.Embed:
        """Format a log record as a Discord embed."""
        if record.levelno >= 40:
            color = discord.Color.red()
        elif record.levelno == 30:
            color = discord.Color.yellow()
        else:
            color = discord.Color.greyple()

        timestamp = record.asctime.split(',')[0]

        log_embed = discord.Embed(
            description=record.message,
            color=color,
            timestamp=datetime.fromisoformat(timestamp)
        )
        log_embed.add_field(name='Level', value=record.levelname)
        log_embed.add_field(name='Module', value=record.module)
        log_embed.add_field(name='Timestamp', value=timestamp)
        
        return log_embed
    

def configure_logging(name: str, filename: str) -> logging.Logger:
    """Retrieve the logger, creating it if necessary.

    Parameters
    ----------
    name : str
        The name of the logger.
    filename : str
        The name of the file to use as a stream.

    Returns
    -------
    logging.Logger
        A logger emitting formatted records 
        to the console and the specified file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_format = '[%(levelname)s] [%(module)s]: %(asctime)s - %(message)s'
    date_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(log_format, datefmt=date_fmt)
    
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def configure_discord_logging(
        name: str,
        bot: commands.Bot,
        channel_id: int
) -> logging.Logger:
    """
    Retrieve the logger and add a handler for sending records
    to the specified Discord channel. 

    Parameters
    ----------
    name : str
        The name of the logger.
    bot : commands.Bot
        The Discord bot instance.
    channel_id : int
        The ID of the Discord channel where logs are sent.

    Returns
    -------
    logging.Logger
        A logger with the added ability to dispatch logging events
        to a Discord channel. 
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    discord_handler = DiscordLogHandler(bot, channel_id)
    discord_handler.setLevel(logging.INFO)
    logger.addHandler(discord_handler)

    return logger

import discord
from discord.ext import commands


class TestableBot(commands.Bot):
    '''
    Class to use instead of base Bot class. Allows the bot to respond to messages
    from other bots. Needed for BDD testing
    '''
    async def process_commands(self, message: discord.Message, /) -> None:
        ctx = await self.get_context(message)
        await self.invoke(ctx)
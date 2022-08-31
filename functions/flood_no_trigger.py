import asyncio
from rich.console import Console

from settings.config import *
from functions.flood import FloodChat
from settings.function import SettingsFunction
from settings.config import color_number

console = Console()

class FloodChatNoTrigger(SettingsFunction):
    """flood in a chat without a trigger"""

    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize

        chat_id = int(console.input('[bold red]id> [/]'))

        self.flood = FloodChat(connect_sessions, initialize=True)
        self.flood.ask()

        self.account_count(connect_sessions)

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                self.start_flood(session, chat_id, reply_msg_id=None)
                for session in self.connect_sessions
            ])
        )
        
    async def start_flood(self, session, chat_id, reply_msg_id):
        if not self.initialize:
            await session.start()

        await self.flood.flood(session, chat_id, reply_msg_id)

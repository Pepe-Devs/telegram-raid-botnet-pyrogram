import json
from pyrogram import Client, idle
import asyncio
from rich.prompt import Prompt, Confirm
from rich.console import Console, Theme

from settings.function import SettingsFunction

import logging
from rich.logging import RichHandler

settings_function = SettingsFunction()

try:
    from sessions.config_api import api_id, api_hash
except:
    settings_function.add_api()

console = Console()

logging.basicConfig(
    level="INFO",
    handlers=[RichHandler()]
)

class ConnectSessions:
    def __init__(self):
        self.initialize = Confirm.ask('[bold]Initialize sessions?')

        self.connect_sessions = []

        with open('sessions/sessions.json', 'r') as json_session:
            sessions = json.load(json_session)['storage_sessions']

            for session in sessions:
                session_name=Client(
                    'session',
                    session_string=session
                    )
                self.connect_sessions.append(session_name)

        if self.initialize:
            asyncio.get_event_loop().run_until_complete(
                asyncio.wait([
                    self.connect_session(number, session)
                    for number, session in enumerate(self.connect_sessions)
                ])
            )

    async def connect_session(self, number, session):
        try:
            await session.start()
            self.connect_sessions.remove(session)
            self.connect_sessions.append(session)

        except Exception as error:
            console.log(f'NOT CONNECTED/{error}')
            self.connect_sessions.remove(session)

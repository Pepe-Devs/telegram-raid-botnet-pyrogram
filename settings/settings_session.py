import json
from pyrogram import Client
import asyncio
from rich.prompt import Prompt, Confirm
from rich.console import Console, Theme

from settings.function import SettingsFunction

settings_function = SettingsFunction()

try:
    from sessions.config_api import api_id, api_hash
except:
    settings_function.add_api()

console = Console()

class ConnectSessions:
    def __init__(self):
        self.initialize = Confirm.ask('[bold]Initialize sessions?')

        self.connect_sessions = []

        with open('sessions/sessions.json', 'r') as json_session:
            sessions = json.load(json_session)['storage_sessions']
            for app in sessions:
                session_name=Client(
                'app',
                api_id=api_id,
                api_hash=api_hash,
                session_string=app)
                self.connect_sessions.append(session_name)

        if self.initialize:
            with console.status("Initializing"):
                asyncio.get_event_loop().run_until_complete(
                    asyncio.wait([
                        self.connect_session(number, session)
                        for number, session in enumerate(self.connect_sessions)
                    ])
                )

    async def connect_session(self, number, app):
        try:
            console.log(f'CONNECT...{number}')
            await app.start()
            console.log(f'CONNECTED/{number}')

            self.connect_sessions.append(app)
            self.connect_sessions.remove(app)

        except Exception as error:
            console.log(f'NOT CONNECTED/{error}')
            self.connect_sessions.remove(app)

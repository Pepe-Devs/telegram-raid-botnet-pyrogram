from pyrogram import Client
from rich.console import Console, Theme
import re
import asyncio

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class SpamBlock(SettingsFunction):
    """checking accounts for spam block"""
    def __init__(self, connect_sessions, initialize):
        self.connect_sessions = connect_sessions
        self.initialize = initialize

        self.permanent_block = []
        self.no_spamblock = []
        self.time_block = []

        for app in self.connect_sessions:
            if not self.initialize:
                app.connect()
            try:
                self.me = app.get_me()
                app.send_message('SpamBot', '/start')

            except Exception as error:
                app.unblock_user(178220800)
                console.print(f'[bold red]ERROR[white bold]: <I tried to unban the bot, try again!>[/] {self.me.first_name} {error}')

            self.checking_block(app)

        console.print(f"""[bold]
perpetual block count: {len(self.permanent_block)}
no spamblock: {len(self.no_spamblock)}
temporary spam block: {len(self.time_block)}
        """)

    def checking_block(self, app):

        self.message = app.get_chat_history('SpamBot', limit=1)

        for msg in self.message:
            if msg.text == '/start':
                self.checking_block(app)

            else:
                try:
                    if msg.text == 'Good news, no limits are currently applied to your account. You’re free as a bird!':
                        console.print(f'[bold green][+][/] [{self.me.first_name}] id:[{self.me.id}]')
                        self.no_spamblock.append(app)

                    else:
                        text = re.findall(r"\d+\s\w+\s\d{4}", msg.text)
                        console.print(f'[bold red][-][/] [{self.me.first_name}] id:[{self.me.id}] = {text[0]}')
                        self.time_block.append(app)

                except:
                    console.print(f'[bold red][-][/] [{self.me.first_name}] id:[{self.me.id}]')
                    self.permanent_block.append(app)

from pyrogram import Client
from rich.console import Console, Theme
import re
import asyncio
from rich.progress import track

from rich import box
from rich.table import Table

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class SpamBlock(SettingsFunction):
    """checking accounts for spam block"""

    def __init__(self, connect_sessions, initialize):
        self.connect_sessions = connect_sessions
        self.initialize = initialize

        self.message_en = 'Good news, no limits are currently applied to your account. You’re free as a bird!'
        self.message_ru = 'Ваш аккаунт свободен от каких-либо ограничений.'

        self.table = Table(
            title='[bold red]SpamBlock',
            box=box.ROUNDED
            )

        self.table.add_column("Name")
        self.table.add_column("Number")
        self.table.add_column("Block")

        for session in track(
            self.connect_sessions,
            '[bold yellow]Verification, please expect...[/]'
        ):
            if not self.initialize:
                session.connect()

            try:
                self.me = session.get_me()
                session.send_message('SpamBot', '/start')

            except Exception as error:
                session.unblock_user(178220800)
                console.print(
                    '[bold red]ERROR[white bold]: <I tried to unban the bot, try again!>[/]',
                    {self.me.first_name},
                    {error}
                )

            self.checking_block(session)

        console.print(self.table)

    def checking_block(self, session):
        messages = session.get_chat_history('SpamBot', limit=1)
        message = [text for text in messages][0]

        if message.text == '/start':
            self.checking_block(session)

        else:
            try:
                if message.text in (self.message_ru, self.message_en):
                    self.table.add_row(
                        self.me.first_name,
                        self.me.phone_number,
                        '[bold green][+][/]'
                    )

                else:
                    text = str(re.findall(r"\d+\s\w+\s\d{4}", message.text)[0])
                    self.table.add_row(
                        self.me.first_name,
                        self.me.phone_number,
                        text
                    )

            except:
                self.table.add_row(
                    self.me.first_name,
                    self.me.phone_number,
                    '[bold red][-][/]'
                )

from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.progress import track
from rich.prompt import Prompt, Confirm
import random

from settings.function import SettingsFunction
from settings.config import first_name
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class TextProfile(SettingsFunction):
    """change biography/nickname"""

    def __init__(self, connect_sessions, initialize):
        self.first_name = first_name
        self.initialize = initialize
        self.connect_sessions = connect_sessions

        name = Confirm.ask(
            '[bold red]to take names from a config?[bold magenta]',
            choices=["y", "n"]
        )

        if not name:
            self.first_name = console.input(
                '[bold red]first name[/]> '
            ).split()

        self.bio = console.input('[bold red]bio[/]> ')
        self.last_name = console.input('[bold red]last name[/]> ')

        for session in track(
            self.connect_sessions,
            description='[bold]CHANGE'
        ):
            self.change_profile(session)

    def change_profile(self, session):

        if not self.initialize:
            session.connect()

        me = session.get_me()

        try:
            session.update_profile(
                    first_name=random.choice(self.first_name),
                    bio=self.bio,
                    last_name=self.last_name
                )

        except Exception as error:
            console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')

from rich.console import Console, Theme
from pyrogram import Client
from rich.prompt import Prompt, Confirm
from time import perf_counter
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number

console = Console(theme=Theme({"repr.number": color_number}))

class Vote(SettingsFunction):
    """voting in the survey"""

    def __init__(self, connect_sessions, initialize):
        self.connect_sessions = connect_sessions
        self.initialize = initialize

        console.print(
            '[magenta]does not work if the survey is a response to another message[/]'
        )

        self.account_count(connect_sessions)

        self.link = console.input(
                '[bold red]link to the message>[/] '
            )

        self.option = int(console.input(
                '[bold red]option number[blue](1-10)[/]: '
            ))-1

        for session in track(
            self.connect_sessions,
            description='[bold]VOTED'
        ):
            self.voited(session)

    def voited(self, session):
        if not self.initialize:
            session.connect()

        me = session.get_me()

        try:
            peer = ''.join(self.link.split('/')[-2:-1])
            post_id = int(self.link.split('/')[-1])

            if peer.isdigit():
                peer = int(f'-100{peer}')

        except Exception as error:
            console.print(
                '[bold red]ERROR[/]:{name} {error}'
                .format(
                    name=me.first_name,
                    error=error
                )
            )

        try:
            session.vote_poll(
                peer,
                post_id,
                self.option
            )

        except Exception as error:
            console.print(f'[bold red]ERROR[/]:{me.first_name} {error}')

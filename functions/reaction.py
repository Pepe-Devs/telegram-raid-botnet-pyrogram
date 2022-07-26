from pyrogram import Client
from rich.console import Console, Theme
import asyncio
from rich.progress import track
from rich.prompt import Confirm
import random

from settings.function import SettingsFunction
from settings.config import color_number, emoji

console = Console(theme=Theme({"repr.number": color_number}))

class ReactionMessage(SettingsFunction):
    """reaction raid"""

    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize
        self.emoji = emoji

        mode = (
            ('adding reactions to a message', self.add_reaction),
            ('reaction flood(on existing messages)', self.flood_reaction)
        )

        for number, function in enumerate(mode, 1):
            console.print(
                '[{number}] {name}'
                .format(
                    number=number,
                    name=function[0]
                ),
                style='bold white'
            )

        choice = int(
            console.input(
                '[bold white]>> [/]'
            ))-1

        self.function = mode[choice][1]

        self.account_count(connect_sessions)

        self.link = console.input('[bold red]link(to any message in the chat)> ')
        self.mix_reacion = Confirm.ask('[bold red]use random reactions?[/]')

        if not self.mix_reacion:
            for number, name in enumerate(self.emoji, 1):
                console.print(
                    f'[{number}] {name}'
                )

            choice = int(console.input(
                '[bold white]>> [/]'
                ))-1

            self.emoji = [self.emoji[choice]]

        asyncio.get_event_loop().run_until_complete(
            asyncio.gather(*[
                    self.reaction(session)
                    for session in self.connect_sessions
                ])
            )

    async def reaction(self, session):
        if not self.initialize:
            await session.connect()

        me = await session.get_me()

        peer = ''.join(self.link.split('/')[-2:-1])
        post_id = int(self.link.split('/')[-1])

        if peer.isdigit():
            peer = int(f'-100{peer}')

        errors_count = 0

        try:
            await self.function(session, peer, post_id)
            console.print(
                f'[{me.first_name}] [bold green]appreciated[/]!'
            )

        except Exception as error:
            errors_count += 1
            console.print(
                    f'[{me.first_name}] [bold red]not rated[/]: {error}'
                )

    async def add_reaction(self, session, peer, post_id):
        await session.send_reaction(
            peer,
            post_id,
            random.choice(
                self.emoji
            )
        )

    async def flood_reaction(self, session, peer, post_id):
        messages = session.get_chat_history(peer)

        async for message in messages:
            try:
                await self.add_reaction(
                    session,
                    peer,
                    message.id
                )

            except Exception as error:
                console.print(error)

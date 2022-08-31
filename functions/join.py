from rich.console import Console, Theme
from pyrogram import Client
import asyncio
from rich.prompt import Prompt, Confirm
from time import perf_counter, sleep
from rich.progress import track

from settings.function import SettingsFunction
from settings.config import color_number
from functions.flood import FloodChat
from settings.config import time_captcha

console = Console(theme=Theme({"repr.number": color_number}))

class Joined(FloodChat):
    """join to chat"""

    def __init__(self, connect_sessions, initialize):
        self.initialize = initialize
        self.connect_sessions = connect_sessions
        self.join_flood = None

        self.account_count(self.connect_sessions)

        console.print(
            '[1] joining a chat/channel',
            '[2] joining a chat via a channel',
            sep='\n',
            style='bold'
        )

        self.mode = console.input(
            '[bold white]>> [/]'
            )

        link = console.input(f'[bold red]link> [/]')

        if '/+' in link:
            self.link = link.replace('/+', '/joinchat/') #/+ криво работает в pyrogram
        elif '/joinchat' in link:
            self.link = link
        else:
            self.link = link.split('/')[3]

        self.settings_join = Prompt.ask(
            '[bold red]speed[bold magenta]',
            choices=["norm", "fast"]
        )

        asyncio.get_event_loop().run_until_complete(self.start_joined())

    async def join_chat(self, session):
        if not self.initialize:
            await session.start()

        me = await session.get_me()

        try:
            if self.mode == '1':
                self.chat = self.link

            else:
                channel = await session.get_chat(self.link)
                self.chat = channel.linked_chat.id

            await session.join_chat(self.chat)

        except Exception as error:
            console.print(f'[bold red]did not join[/]: {error}')

    async def start_joined(self):
        if self.settings_join == 'norm':

            self.captcha = Confirm.ask('[bold red]captcha?')
            time_normal = int(console.input('[bold blue]delay>[/] '))

            for session in track(
                self.connect_sessions,
                description='[bold]JOIN'
            ):

                await self.join_chat(session)
                await asyncio.sleep(time_normal)

                if self.captcha:
                    await self.solve_captcha(session, self.chat)

        elif self.settings_join == 'fast':
            self.join_flood = Confirm.ask('[bold red]flood after joining?[/]')

            if self.join_flood:
                initialize = True
                flood = FloodChat(self.connect_sessions, initialize)
                flood.ask()

            joined = 0
            start = perf_counter()

            tasks = await asyncio.gather(*[
                self.join_chat(session)
                for session in self.connect_sessions
            ])

            for result in tasks:
                joined += 1

            join_time = round(perf_counter() - start, 2)
            console.print(f"[+] {joined} bots joined [yellow]{join_time}[/]s")

        if self.join_flood:
            await asyncio.gather(*[
                flood.flood(session, self.chat, reply_msg_id=None)
                for session in self.connect_sessions
            ])


    async def solve_captcha(self, session, chat_id):
        sleep(time_captcha)

        message = session.get_chat_history(chat_id, limit=5)

        async for msg in message:
            try:
                callback = msg.reply_markup \
                    .inline_keyboard[0][0].callback_data

                await session.request_callback_answer(
                    chat_id,
                    msg.id,
                    callback
                )
            except:
                pass
